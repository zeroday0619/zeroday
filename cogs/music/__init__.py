import asyncio
import discord
import traceback
import itertools
import re
import sys
from discord.ext.commands import Context
from validator_collection import checkers
from discord.ext import commands
from discord.ext.commands import Bot
from discord.ext.commands import Cog
from discord.ext.commands import NoPrivateMessage
from app.ext.music.option import EmbedSaftySearch
from app.ext.music.option import adult_filter
from app.ext.music.YTDLSource import YTDLSource
from app.ext.music.Player import Player
from app.controller.logger import Logger
from app.ext.music.option import (
    embed_ERROR,
    embed_queued,
    embed_value,
    InvalidVoiceChannel,
    VoiceConnectionError,
)

__version__ = "3.5.0"


class YTDLError(Exception):
    pass


@Logger.set()
def cleanText(readData):
    text = re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]', '', readData)
    return text


class CoreMusic(Cog):
    """뮤직 모듈"""

    __slots__ = ("bot", "players", "logger")

    def __init__(self, bot: Bot):
        self.logger = Logger.generate_log()
        self.bot = bot
        self.players = {}
        self.cog_version = __version__
        self.ver_string = "Ver"

    @Logger.set()
    async def cleanup(self, guild):
        try:
            await guild.voice_client.disconnect()
        except AttributeError as e:
            raise e

        try:
            for source in self.players[guild.id].queue._queue:
                source.cleanup()
            del self.players[guild.id]
        except KeyError as e:
            raise e

    @staticmethod
    @Logger.set()
    async def __local_check(ctx):
        if not ctx.guild:
            raise NoPrivateMessage
        return True

    @staticmethod
    @Logger.set()
    async def __error(ctx, error):
        if isinstance(error, NoPrivateMessage):
            try:
                return await ctx.send("이 Command 는 DM 에서 사용할 수 없습니다")
            except discord.HTTPException as e:
                raise e

        elif isinstance(error, InvalidVoiceChannel):
            await ctx.send(
                "Voice Channel 연결중 Error 가 발생하였습니다\n 자신이 Voice Channel에 접속되어 있는 지 확인 바랍니다."
            )

        await ctx.send("ERROR: Ignoring exception in command {}".format(ctx.command))

        Logger.generate_log().error("Ignoring exception in command {}".format(ctx.command))
        Logger.generate_log().exception(error)

    @Logger.set()
    def get_player(self, ctx):
        """
        :rtype: object
        """
        try:
            player = self.players[ctx.guild.id]
        except KeyError:
            player = Player(ctx)
            self.players[ctx.guild.id] = player

        return player


class Music(CoreMusic):
    """Music"""
    __slots__ = ("bot", "players", "logger")

    def __init__(self, bot: Bot):
        self.logger = Logger.generate_log()
        super(Music, self).__init__(bot)

    @staticmethod
    @Logger.set()
    async def check(ctx, search):
        if checkers.is_url(search):
            source = await YTDLSource.Search(ctx, search, download=False, loop=ctx.bot.loop)
            return source
        else:
            search_text = search
            serc = search_text.replace(":", "")
            source = await YTDLSource.Search(ctx, serc, download=False, loop=ctx.bot.loop)
            return source

    @Logger.set()
    async def pause_embed(self, ctx):
        nx = discord.Embed(
            title="Music",
            description=f"```css\n{ctx.author} : 일시중지.\n```",
            color=discord.Color.blurple(),
        ).add_field(name=self.ver_string, value=self.cog_version)
        return nx

    @Logger.set()
    async def resume_embed(self, ctx):
        nx = discord.Embed(
            title="Music",
            description=f"```css\n**{ctx.author}** : 다시재생.\n```",
            color=discord.Color.blurple(),
        ).add_field(name=self.ver_string, value=self.cog_version)
        return nx

    @Logger.set()
    async def volume_embed(self, ctx, vol):
        ix = discord.Embed(
            title="Music",
            description=f"```{ctx.author}: Set the volume to {vol}%```",
            color=discord.Color.blurple(),
        ).add_field(name=self.ver_string, value=self.cog_version)
        return ix

    @Logger.set()
    async def now_playing_embed(self, vc):
        ex = discord.Embed(
            title=f"Now Playing: ```{vc.source.title}```",
            description=f"requested by @{vc.source.requester}",
            color=discord.Color.blurple(),
        ).add_field(name=self.ver_string, value=self.cog_version)
        return ex

    @Logger.set()
    async def queue_info_embed(self, player):
        upcoming = list(itertools.islice(player.queue._queue, 0, 50))
        fmt = "\n".join(f'```css\n{_["title"]}\n```' for _ in upcoming)
        embed_queue = discord.Embed(
            title=f"Upcoming - Next **{len(upcoming)}**",
            description=fmt,
            color=discord.Color.blurple(),
        ).add_field(name=self.ver_string, value=self.cog_version)
        return embed_queue

    @commands.group(name="music", aliases=["m"])
    async def _music(self, ctx):
        """
        ```markdown
        Music
        --------------------------------------------------
        |   Type   | aliases |      description
        |:--------:|:-------:|----------------------------
        |  connect |   join  |보이스 채널에 들어갑니다
        |   play   |   None  |유튜브 (재생) [Search]
        | play_list|   ml    |유튜브 (재생) playlist [Search]
        | search   |   None  |유튜브 검색 (재생) [Search]
        |   stop   |  None   |종료
        |   loop   |    lp   |반복 재생
        |   pause  |   None  |일시 중지
        |  resume  |   None  |다시 재생
        |   skip   |  None   |건너 뛰기
        |  remove  |   rm    |playlist 제거
        |  queue   |    q    |재생 목록
        | shuffle  |   sff   |shuffle
        | current  |    np   |재생중인 컨텐츠 정보 보기
        |  volume  |   vol   |사운드 크기 조절
        |   stop   |  None   |종료
        ```
        """
        if ctx.invoked_subcommand is None:
            help_cmd = self.bot.get_command("help")
            await ctx.invoke(help_cmd, "music")

    @_music.command(name="connect", aliases=["join", "j"])
    async def connect_(self, ctx, *, channel: discord.VoiceChannel = None):
        """보이스 채널에 들어갑니다"""
        if not channel:
            try:
                channel = ctx.author.voice.channel
            except AttributeError as r2:
                await ctx.send("'Voice channel'에 연결하지 못하였습니다.\n 유효한 'Voice channel'에 자신이 들어와 있는지 확인바랍니다.")
                raise InvalidVoiceChannel(f"{r2.__class__.__module__}: {r2.__class__.__name__}")

        vc = ctx.voice_client

        if vc:
            if vc.channel.id == channel.id:
                return
            try:
                await vc.move_to(channel)
            except asyncio.TimeoutError as TError:
                await ctx.send(f"Moving to channel: <{str(channel)}> timed out")
                raise VoiceConnectionError(f"{TError.__class__.__module__}: {TError.__class__.__name__}")
        else:
            try:
                await channel.connect()
            except asyncio.TimeoutError as TError2:
                await ctx.send(f"Connecting to channel: <{str(channel)}> timed out")
                raise VoiceConnectionError(f"{TError2.__class__.__module__}: {TError2.__class__.__name__}")

        await ctx.send(
            "```css\nConnected to **{}**\n```".format(str(channel)), delete_after=10
        )

    @_music.command(name="loop", aliases=["lp"])
    async def _loop(self, ctx, mode: str):
        """반복 재생"""
        player = self.get_player(ctx)

        if not player:
            return

        modes = ["current", "all", "disable"]
        if not mode in modes:
            return await ctx.send(
                f"invalid arg: {mode}\nuse: {'/'.join(modes)}", delete_after=5
            )

        if mode == "disable":
            player.loop = False
        else:
            player.loop = True

        await ctx.send(f"Player repeat: **{mode}**", delete_after=5)

    @_music.command(name="play", aliases=["music", "p"])
    async def play_(self, ctx, *, search: str):
        """재생"""
        await ctx.trigger_typing()
        vc = ctx.voice_client
        if not vc:
            await ctx.invoke(self.connect_)

        player = self.get_player(ctx)

        source = await self.check(ctx=ctx, search=search)

        if await adult_filter(search=cleanText(source.title), loop=ctx.bot.loop) == 1:
            embed_two = EmbedSaftySearch(data=str(search))
            await ctx.send(embed=embed_two)
            await self.cleanup(ctx.guild)
        else:
            await player.queue.put(source)

    @_music.command(name="play_list", aliases=["ml"])
    async def create_playlist_play(self, ctx, *, search: str):
        """재생"""
        await ctx.trigger_typing()

        vc = ctx.voice_client
        if not vc:
            await ctx.invoke(self.connect_)

        if await adult_filter(search=cleanText(search), loop=ctx.bot.loop) == 1:
            embed_two = EmbedSaftySearch(data=str(search))
            await ctx.send(embed=embed_two)
        else:
            player = self.get_player(ctx)
            source = await YTDLSource.create_playlist(ctx, search, download=False, loop=ctx.bot.loop)
            for ix in source:
                await player.queue.put(ix)

    @_music.command(name="pause")
    async def pause_(self, ctx):
        """일시중지"""
        vc = ctx.voice_client
        if not vc or not vc.is_playing():
            return await ctx.send(embed=embed_ERROR, delete_after=20)
        elif vc.is_paused():
            return

        nx = self.pause_embed(ctx=ctx)
        vc.pause()

        await ctx.send(embed=nx, delete_after=5)

    @_music.command(name="resume")
    async def resume_(self, ctx):
        """다시 재생"""
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.send(embed=embed_ERROR, delete_after=20)
        elif not vc.is_paused():
            return

        nx = self.resume_embed(ctx=ctx)
        vc.resume()

        await ctx.send(nx, delete_after=5)

    @_music.command(name="skip")
    async def skip_(self, ctx):
        """스킵"""
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.send(embed=embed_ERROR, delete_after=20)

        if vc.is_paused():
            pass
        elif not vc.is_playing():
            return

        vc.stop()
        await ctx.send(f"```css\n{ctx.author} : 스킵!.\n```", delete_after=5)

    @_music.command(name="remove", aliases=["rm"])
    async def _remove(self, ctx, index: int):
        player = self.get_player(ctx)
        if len(player.queue._queue) == 0:
            return await ctx.send("Empty queue", delete_after=10)

        player.queue.remove(index - 1)
        await ctx.send("Success delete song", delete_after=10)

    @_music.command(name="shuffle", aliases=["sff"])
    async def _shuffle(self, ctx):
        player = self.get_player(ctx)
        if len(player.queue._queue) == 0:
            return await ctx.send("Empty queue", delete_after=10)

        player.queue.shuffle()
        await ctx.send("Success")

    @_music.command(name="queue", aliases=["q", "playlist"])
    async def queue_info(self, ctx):
        """재생목록"""

        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.send(embed=embed_ERROR, delete_after=20)

        player = self.get_player(ctx)
        if player.queue.empty():
            return await ctx.send(embed=embed_queued)

        ox = await self.queue_info_embed(player=player)
        await ctx.send(embed=ox)

    @_music.command(
        name="now_playing", aliases=["np", "current", "playing"]
    )
    async def now_playing_(self, ctx):
        """재생중인 컨텐츠 정보 보기"""
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.send(embed=embed_ERROR, delete_after=20)

        player = self.get_player(ctx)
        if not player.current:
            return await ctx.send(embed=embed_ERROR)

        try:
            await player.np.delete()
        except discord.HTTPException:
            pass

        ex = await self.now_playing_embed(vc=vc)
        player.np = await ctx.send(embed=ex)

    @_music.command(name="volume", aliases=["vol"])
    async def change_volume(self, ctx, *, vol: float):
        """사운드 크기 조절"""
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.send(embed=embed_ERROR, delete_after=10)

        if not 0 < vol < 101:
            return await ctx.send(embed_value)

        player = self.get_player(ctx)

        if vc.source:
            vc.source.volume = vol / 100

        player.volume = vol / 100
        ix = await self.volume_embed(ctx=ctx, vol=vol)
        await ctx.send(embed=ix, delete_after=10)

    @_music.command(name="stop")
    async def stop_(self, ctx):
        """stop"""
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.send(embed=embed_ERROR, delete_after=20)

        await self.cleanup(ctx.guild)


@Logger.set()
def setup(bot: Bot):
    bot.add_cog(Music(bot))