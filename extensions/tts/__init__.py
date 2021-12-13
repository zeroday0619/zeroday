import discord
from discord.ext import commands
from discord import PCMVolumeTransformer, VoiceProtocol, Member
from discord.ext.commands import Context
from discord.ext.commands import Bot

from io import BytesIO
from shlex import split
from subprocess import PIPE, Popen
from discord.opus import Encoder

from extensions.tts._kakao import KakaoOpenAPI
from app.controller.logger import Logger
from io import BytesIO
from tempfile import TemporaryFile
from typing import Optional


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
        self.voice = None
        self.open_api = KakaoOpenAPI()

    @Logger.set()
    def is_joined(self, member: Member):
        if not member.voice:
            raise

        return self.voice and self.voice.channel.id == member.voice.channel.id

    @Logger.set()
    async def join(self, member: discord.Member):
        # Joining the already joined channel is a NOP.
        if self.is_joined(member):
            return

        channel = member.voice.channel
        try:
            if self.voice.is_playing():
                raise

            await self.voice.move_to(channel)
        except AttributeError:
            self.voice = await channel.connect()
            
    @Logger.set()
    async def _text_to_speech(self, source, ctx: Context):
        rep = self.open_api.speak_data_generator(source)
        byt = await self.open_api.text_to_speech(rep)

        if not self.voice.is_playing():
            Logger.generate_log().info("O")
            self.voice.play(PCMVolumeTransformer(FFmpegPCMAudio(byt, pipe=True, options='-loglevel "quiet"'), volume=150))
        else:
            Logger.generate_log().info("X")
            await ctx.send(f"{ctx.author.display_name}님 죄송하지만 TTS 재생 중에 TTS 명령어를 사용할 수 없습니다.", delete_after=60)


    @commands.command(name="tts", aliases=["t", "-", "=", "#", "%", "*", "`"])
    @commands.check(blockJam_mini)
    async def talk(self, ctx: Context, *, text: str):
        await self.join(ctx.author)
        await self._text_to_speech(f"{ctx.author.display_name}님의 메시지. {text}", ctx)


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
