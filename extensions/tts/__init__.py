import discord
import asyncio, aiofile
from discord.ext import commands
from discord import VoiceChannel, VoiceClient, FFmpegPCMAudio, AudioSource
from discord.ext.commands import Context
from discord.ext.commands import Bot
from extensions.tts._kakao import KakaoOpenAPI
from app.controller.logger import Logger
from io import BytesIO
from cogs.music import CoreMusic
from tempfile import TemporaryFile


class TextToSpeech(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.voice = None
        self.open_api = KakaoOpenAPI()

    def is_joined(self, member: discord.Member):
        """ Check if the bot is currently in the same voice channel as a member.
        :param member: The target member to compare channels against.
        :type  member: discord.Member
        :returns: `True` if the bot is in a voice channel, and that channel has
                  the same ID as that of the member.
        :rtype:   bool
        :raises NoVoice: An error is raised if the member is not joinable; that
                         is, the member is not in a voice channel.
        """
        if not member.voice:
            raise

        return (self.voice and self.voice.channel.id == member.voice.channel.id)

    async def join(self, member: discord.Member):
        """ Join the specified member in their voice channel.
        :param member: The target member to join.
        :type  member: discord.Member
        :raises NoVoice: This error is propogated from `is_joined()`.
        :raises BadVoice: If the bot is currently playing sound in a different
                          channel, this error is raised.
        :raises discord.DiscordException: Errors from the Discord connection
                                          methods are propogated.
        """
        # Joining the already joined channel is a NOP.
        if self.is_joined(member):
            return

        channel = member.voice.channel
        try:
            if self.voice.is_playing():
                raise

            # If the bot is waiting in a valid voice channel, the voice client
            # can be moved to the new channel rather than connecting anew.
            await self.voice.move_to(channel)
        except AttributeError:
            # The voice client must be `None` or invalid; create a new one.
            self.voice = await channel.connect()

    @Logger.set()
    async def _text_to_speech(self, source):
        rep = self.open_api.speak_data_generator(source)
        byt = await self.open_api.text_to_speech(rep)
        data = BytesIO(byt)
        data.seek(0)
        with TemporaryFile() as file:
            file.write(data.read())
            file.seek(0)
            if not self.voice.is_playing():
                Logger.generate_log().info("x")
                self.voice.play(FFmpegPCMAudio(source=file, pipe=True))

    @commands.command("t")
    async def talk(self, ctx: Context, *, text: str):
        """ synthesize the given text in your voice channel """
        await self.join(ctx.author)
        await self._text_to_speech(text)

    @commands.command("disconnect")
    async def bye(self, ctx: Context):
        """ disconnect the bot from your voice channel """
        # If the bot is not in the user's channel, silently NOP.
        if not self.is_joined(ctx.author):
            return
        if self.voice.is_playing():
            raise

        await self.voice.disconnect()
        self.voice = None

def setup(bot: Bot):
    bot.add_cog(TextToSpeech(bot))
