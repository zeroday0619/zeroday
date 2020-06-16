import asyncio
import discord
import traceback
import itertools
import sys

from discord.ext import commands
from discord.ext.commands import Bot
from discord.ext.commands import Cog
from discord.ext.commands import NoPrivateMessage
from .ext.option import EmbedSaftySearch
from .ext.option import adult_filter
from .ext.performance import run_in_threadpool
from .ext.filter import safe
from .ext.YTDLSource import YTDLSource
from .ext.Player import Player
from .ext.option import embed_ERROR, embed_queued, embed_value, InvalidVoiceChannel, VoiceConnectionError


class music(Cog):
    """뮤직 모듈"""
    __slots__ = ('bot', 'players')

    def __init__(self, bot: Bot):
        self.bot = bot
        self.players = {}
        self.buildVer = "20200616 RC 0843"
        self.verstring = "Ver"

    async def cleanup(self, guild):
        try:
            await guild.voice_client.disconnect()
        except AttributeError:
            pass

        try:
            for source in self.players[guild.id].queue._queue:
                source.cleanup()
        except KeyError:
            pass

        try:
            del self.players[guild.id]
        except KeyError:
            pass

    @staticmethod
    async def __local_check(ctx):
        if not ctx.guild:
            raise NoPrivateMessage
        return True

    @staticmethod
    async def __error(ctx, error):
        if isinstance(error, NoPrivateMessage):
            try:
                return await ctx.send("이 Command 는 DM 에서 사용할 수 없습니다")
            except discord.HTTPException:
                pass

        elif isinstance(error, InvalidVoiceChannel):
            await ctx.send("Voice Channel 연결중 Error 가 발생하였습니다\n 자신이 Voice Channel에 접속되어 있는 지 확인 바랍니다.")

        print('Ignoring exception in command {}'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

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

    @commands.group(name="music", aliases=['m'])
    async def _music(self, ctx):
        """
        ```markdown
        Music
        -----------------------------------------------
        |   Type   | aliases |      description
        |:--------:|:-------:|-------------------------
        |  connect |   join  |보이스 채널에 들어갑니다
        |   play   |   None  |재생 [Search]
        |   loop   |    lp   |반복 재생
        |   pause  |   None  |일시 중지
        |  resume  |   None  |다시 재생
        |   skip   |  None   |건너 뛰기
        |  queue   |    q    |재생 목록
        | current  |    np   |재생중인 컨텐츠 정보 보기
        |  volume  |   vol   |사운드 크기 조절
        |   stop   |  None   |종료

        ```
		"""
        if ctx.invoked_subcommand is None:
            help_cmd = self.bot.get_command('help')
            await ctx.invoke(help_cmd, 'music')

    @_music.command(name='connect', aliases=['join', 'j'])
    async def connect_(self, ctx, *, channel: discord.VoiceChannel = None):
        """보이스 채널에 들어갑니다"""
        if not channel:
            try:
                channel = ctx.author.voice.channel
            except AttributeError as r2:
                await ctx.send("Error: {}".format(str(r2)))
                raise InvalidVoiceChannel(
                    "Voice channel에 연결하지 못하였습니다.\n 유효한 Voice Channel과 자신이 Voice Channel에 들어와 있는지 확인바랍니다.")
        vc = ctx.voice_client

        if vc:
            if vc.channel.id == channel.id:
                return
            try:
                await vc.move_to(channel)
            except asyncio.TimeoutError as TError:
                await ctx.send("Error: {}".format(str(TError)))
                raise VoiceConnectionError("Moving to channel: <{}> timed out".format(str(channel)))
        else:
            try:
                await channel.connect()
            except asyncio.TimeoutError as TError2:
                await ctx.send("Error: {}".format(str(TError2)))
                raise VoiceConnectionError("Connecting to channel: <{}> timed out".format(str(channel)))

        embed_join = (
            discord.Embed(
                title="Music",
                description='```css\nConnected to **{}**\n```'.format(str(channel)),
                color=discord.Color.blurple()
            )
                .add_field(name=self.verstring, value=self.buildVer)
        )
        await ctx.send(embed=embed_join, delete_after=10)

    @_music.command(name="loop", aliases=['lp'])
    async def _loop(self, ctx, mode: str):
        """반복 재생"""

        player = self.get_player(ctx)

        if not player:
            return

        modes = ["current", "all", "disable"]
        if not mode in modes:
            return await ctx.send(f"invalid arg: {mode}\nuse: {'/'.join(modes)}", delete_after=5)

        if mode == "disable":
            player.repeat = None
        else:
            player.repeat = mode
        await ctx.send(f"Player repeat: **{mode}**", delete_after=5)

    @_music.command(name='play', aliases=['music', 'p'])
    async def play_(self, ctx, *, search: str):
        """재생"""
        await ctx.trigger_typing()

        if await adult_filter(search=str(search)) == 1:
            embed_one = EmbedSaftySearch(data=str(search))
            await ctx.send(embed=embed_one)
        else:
            vc = ctx.voice_client
            if not vc:
                await ctx.invoke(self.connect_)
            player = self.get_player(ctx)
            source = await YTDLSource.Search(ctx, search, download=True)
            if await adult_filter(search=source.title) == 1:
                embed_two = EmbedSaftySearch(data=str(search))
                await ctx.send(embed=embed_two)
                await self.cleanup(ctx.guild)
            await player.queue.put(source)

    @_music.command(name='pause')
    async def pause_(self, ctx):
        """일시중지"""
        vc = ctx.voice_client

        if not vc or not vc.is_playing():
            return await ctx.send(embed=embed_ERROR, delete_after=20)
        elif vc.is_paused():
            return
        embed_pause = (
            discord.Embed(
                title="Music",
                description=f'```css\n{ctx.author} : 일시중지.\n```',
                color=discord.Color.blurple()
            )
                .add_field(name=self.verstring, value=self.buildVer)
        )

        vc.pause()
        await ctx.send(embed=embed_pause, delete_after=5)

    @_music.command(name='resume')
    async def resume_(self, ctx):
        """다시 재생"""
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.send(embed=embed_ERROR, delete_after=20)
        elif not vc.is_paused():
            return

        vc.resume()
        embed_resume = (
            discord.Embed(
                title="Music",
                description=f'```css\n**{ctx.author}** : 다시재생.\n```',
                color=discord.Color.blurple()
            )
                .add_field(name=self.verstring, value=self.buildVer)
        )

        await ctx.send(embed_resume, delete_after=5)

    @_music.command(name='skip')
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
        embed_skip = (
            discord.Embed(
                title="Music",
                description=f'```css\n**{ctx.author}** : 스킵!.\n```',
                color=discord.Color.blurple()
            )
                .add_field(name=self.verstring, value=self.buildVer)
        )

        await ctx.send(embed=embed_skip, delete_after=5)

    @_music.command(name='queue', aliases=['q', 'playlist'])
    async def queue_info(self, ctx):
        """재생목록"""

        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.send(embed=embed_ERROR, delete_after=20)

        player = self.get_player(ctx)
        if player.queue.empty():
            return await ctx.send(embed=embed_queued)

        upcoming = list(itertools.islice(player.queue._queue, 0, 50))
        fmt = '\n'.join(f'```css\n{_["title"]}\n```' for _ in upcoming)
        embed_queue = (
            discord.Embed(
                title=f'Upcoming - Next **{len(upcoming)}**',
                description=fmt,
                color=discord.Color.blurple()
            )
            .add_field(name=self.verstring, value=self.buildVer)
        )

        await ctx.send(embed=embed_queue)

    @_music.command(name='now_playing', aliases=['np', 'current', 'currentsong', 'playing'])
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
        embed_now_playing = (
            discord.Embed(
                title=f'```css\n**Now Playing:** {vc.source.title}```',
                description=f'requested by `{vc.source.requester}`',
                color=discord.Color.blurple()
            )
                .add_field(name=self.verstring, value=self.buildVer)
        )
        player.np = await ctx.send(embed=embed_now_playing)

    @_music.command(name='volume', aliases=['vol'])
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
        embed_now_playing = (
            discord.Embed(
                title="Music",
                description=f'```{ctx.author}: Set the volume to {vol}%```',
                color=discord.Color.blurple()
            )
                .add_field(name=self.verstring, value=self.buildVer)
        )

        await ctx.send(embed=embed_now_playing, delete_after=10)

    @_music.command(name='stop')
    async def stop_(self, ctx):
        """stop"""
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.send(embed=embed_ERROR, delete_after=20)

        await self.cleanup(ctx.guild)


def setup(bot: Bot):
    bot.add_cog(music(bot))
