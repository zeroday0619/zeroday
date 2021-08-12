import discord
from discord.ext import commands
from discord import FFmpegPCMAudio, PCMVolumeTransformer, VoiceProtocol, VoiceChannel, Member
from discord.ext.commands import Context
from discord.ext.commands import Bot
from discord.member import VoiceState
from extensions.tts._kakao import KakaoOpenAPI
from app.controller.logger import Logger
from io import BytesIO
from tempfile import TemporaryFile
from typing import Optional


def blockJam_mini(ctx: Context):
    return ctx.message.author.id != 669558223329820702


class TextToSpeech(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.voice: Optional[VoiceProtocol] = None
        self.open_api = KakaoOpenAPI()

    @Logger.set()
    def is_joined(self, member: Member):
        if not member.voice:
            raise RuntimeWarning("Unknown Type")

        return self.voice and self.voice.channel.id == member.voice.channel.id

    @Logger.set()
    async def join(self, member: discord.Member):
        # Joining the already joined channel is a NOP.
        if self.is_joined(member):
            raise RuntimeWarning(f"{member} is already joined.")

        if type(self.voice) is VoiceProtocol:
            raise RuntimeWarning("Unknown Type")

        channel: VoiceChannel = member.voice.channel
        try:

            if self.voice.is_playing():
                raise RuntimeWarning("Already playing")

            await self.voice.move_to(channel)
        except AttributeError as e:
            self.voice = await channel.connect()
            raise RuntimeWarning(e)
            
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
                self.voice.play(PCMVolumeTransformer(FFmpegPCMAudio(source=file, pipe=True), volume=150), after=file.close())

    @commands.command(name="tts", aliases=["t", "-", "=", "#", "%", "*", "`"])
    @commands.check(blockJam_mini)
    async def talk(self, ctx: Context, *, text: str):
        try:
            if not self.is_joined(ctx.author):
                await self.join(ctx.author)

            await self._text_to_speech(f"{ctx.author.display_name}님이 말합니다. "+text)
        except Exception as e:
            raise RuntimeError(e)

    @commands.command("disconnect")
    @commands.check(blockJam_mini)
    async def bye(self, ctx: Context):
        if not self.is_joined(ctx.author):
            return

        if self.voice.is_playing():
            raise

        await self.voice.disconnect()
        self.voice = None


def setup(bot: Bot):
    bot.add_cog(TextToSpeech(bot))
