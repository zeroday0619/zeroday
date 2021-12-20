import asyncio
import discord

from discord.ext import commands
from discord import PCMVolumeTransformer, Member, VoiceClient
from discord.ext.commands import Context
from discord.ext.commands import Bot

from app.error.music import InvalidVoiceChannel
from app.error.music import VoiceConnectionError

from io import BytesIO
from shlex import split
from subprocess import PIPE, Popen
from discord.opus import Encoder
from app.ext.music.option import adult_filter
from extensions.tts._kakao import KakaoOpenAPI
from app.controller.logger import Logger
from io import BytesIO
from tempfile import TemporaryFile
from typing import Dict, Optional
from app.module import RegexFilter

class FFmpegPCMAudio(discord.AudioSource):
    """Reimplementation of discord.FFmpegPCMAudio with source: bytes support
    Original Source: https://github.com/Rapptz/discord.py/issues/5192"""

    def __init__(
        self,
        source,
        *,
        executable="ffmpeg",
        pipe=False,
        stderr=None,
        before_options=None,
        options=None
    ):
        args = [executable]
        if isinstance(before_options, str):
            args.extend(split(before_options))

        args.append("-i")
        args.append("-" if pipe else source)
        args.extend(("-f", "s16le", "-ar", "48000", "-ac", "2", "-loglevel", "warning"))

        if isinstance(options, str):
            args.extend(split(options))

        args.append("pipe:1")

        self._stdout = None
        self._process = None
        self._stderr = stderr
        self._process_args = args
        self._stdin = source if pipe else None

    def _create_process(self) -> BytesIO:
        stdin, stderr, args = self._stdin, self._stderr, self._process_args
        self._process = Popen(args, stdin=PIPE, stdout=PIPE, stderr=stderr)
        return BytesIO(self._process.communicate(input=stdin)[0])

    def read(self) -> bytes:
        if self._stdout is None:
            # This function runs in a voice thread, so we can afford to block
            # it and make the process now instead of in the main thread
            self._stdout = self._create_process()

        ret = self._stdout.read(Encoder.FRAME_SIZE)
        return ret if len(ret) == Encoder.FRAME_SIZE else b""

    def cleanup(self):
        process = self._process
        if process is None:
            return

        process.kill()
        if process.poll() is None:
            process.communicate()


        self._process = None



def blockJam_mini(ctx: Context):
    return ctx.message.author.id != 669558223329820702


class TextToSpeech(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.voice: Optional[Dict[int, VoiceClient]] = {}
        self.open_api = KakaoOpenAPI()
        
    @classmethod
    @Logger.set()
    async def regex_filter(cls, ctx: Context, source: str):
        tool = RegexFilter()
        try:
            if await tool.check(source=source):
                cls.logger.info(f"차단: {source}")
                try:
                    embed = EmbedSaftySearch(data=str(source))
                    await ctx.send(embed=embed)
                except Exception as e:
                    cls.logger.debug(msg=e)
                    pass
                return True
            else:
                return False
        except Exception as e:
            cls.logger.debug(msg=e)
            return False
        
    @Logger.set()
    def is_joined(self, ctx: Context, member: Member):
        """
        Checks if member is in a voice channel.
        Args:
            ctx: ApplicationContext
            member: ctx.author or discord.Member
        """
        if not member.voice:
            raise

        return (
            self.voice.get(ctx.author.guild.id)
            and self.voice.get(ctx.author.guild.id) is not None
            and self.voice.get(ctx.author.guild.id).channel.id
            == member.voice.channel.id
        )

    @Logger.set()
    async def join(self, ctx: Context):
        # Joining the already joined channel is a NOP.
        """Joins a voice channel."""
        if self.is_joined(ctx, ctx.author):
            return
        try:
            channel = ctx.author.guild._voice_states[ctx.author.id].channel
        except AttributeError:
            await ctx.respond(
                content="'Voice channel'에 연결하지 못하였습니다.\n 유효한 'Voice channel'에 자신이 들어와 있는지 확인바랍니다."
            )
            raise InvalidVoiceChannel(message="'Voice channel'에 연결하지 못하였습니다.")
        vc = ctx.guild.voice_client
        if vc:
            if vc.channel.id == channel.id:
                return
            try:
                _voice = self.voice[ctx.author.guild.id]
                await _voice.move_to(channel)
            except asyncio.TimeoutError:
                await ctx.respond(
                    content=f"Moving to channel: <{str(channel)}> timed out"
                )
                raise VoiceConnectionError(
                    f"Moving to channel: <{str(channel)}> timed out"
                )
        else:
            try:
                self.voice[ctx.author.guild.id] = await channel.connect()
            except asyncio.TimeoutError:
                await ctx.respond(
                    content=f"Connecting to channel: <{str(channel)}> timed out"
                )
                raise VoiceConnectionError(
                    message=f"Connecting to channel: <{str(channel)}> timed out"
                )
            
    @Logger.set()
    async def _text_to_speech(self, source, ctx: Context):
        vc = ctx.guild.voice_client
        if not vc:
            await ctx.invoke(self.join)

        status = await self.open_api.safe.check(self.open_api.safe.cleanText(source))
        st = await adult_filter(self.open_api.safe.cleanText(source), loop=self.bot.loop)
        if not status:
            if st == 1:
                rep = self.open_api.speak_data_generator("전기통신사업법 및 정보통신망법에 따라 유해 단어를 차단하였습니다.")
            elif st == 0:
                if await cls.regex_filter(ctx=ctx, source=data['title']):
                    rep = self.open_api.speak_data_generator("전기통신사업법 및 정보통신망법에 따라 유해 단어를 차단하였습니다.")
                else:
                    rep = self.open_api.speak_data_generator(source)
            else:
                rep = self.open_api.speak_data_generator("시스템 에러")
        else:
            rep = self.open_api.speak_data_generator("전기통신사업법 및 정보통신망법에 따라 유해 단어를 차단하였습니다.")

        byt = await self.open_api.text_to_speech(rep)

        if not self.voice[ctx.author.guild.id].is_playing():
            Logger.generate_log().info("O")
            self.voice[
                ctx.author.guild.id
            ].play(
                PCMVolumeTransformer(
                    FFmpegPCMAudio(
                        byt, 
                        pipe=True, 
                        options='-loglevel "quiet"'
                        ), 
                    volume=150
                )
            )
        else:
            Logger.generate_log().info("X")
            await ctx.send(f"{ctx.author.display_name}님 죄송하지만 TTS 재생 중에 TTS 명령어를 사용할 수 없습니다.", delete_after=60)


    @commands.command(name="tts", aliases=["t", "-", "=", "#", "%", "*", "`"])
    @commands.check(blockJam_mini)
    async def talk(self, ctx: Context, *, text: str):
        await self.join(ctx)
        await self._text_to_speech(text, ctx)


    @commands.command("disconnect")
    @commands.check(blockJam_mini)
    async def bye(self, ctx: Context):
        """Disconnects from voice channel."""
        if not self.voice.get(ctx.author.guild.id):
            return
        await self.voice[ctx.author.guild.id].disconnect()
        del self.voice[ctx.author.guild.id]


def setup(bot: Bot):
    bot.add_cog(TextToSpeech(bot))
