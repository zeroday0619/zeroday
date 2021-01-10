import re
import discord

from cogs.music._core_music import CoreMusic

from discord.ext import commands
from discord.ext.commands import Bot, Context
from cogs.music._music_sys import (
    connect_voice_channel,
    play_loop,
    play_music,
    play_youtube_playlist,
    pause_play,
    replay,
    skip_song,
    remove_song,
    shuffle,
    get_playlist,
    playing_song,
    change_player_volume,
    play_stop
)

from app.controller.logger import Logger


class Music(CoreMusic):
    """Music"""
    __slots__ = ("bot", "players", "logger")

    def __init__(self, bot: Bot):
        self.logger = Logger.generate_log()
        super(Music, self).__init__(bot)

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
    async def connect_(self, ctx: Context, *, channel: discord.VoiceChannel = None):
        """Voice Channel 연결"""
        await connect_voice_channel(ctx=ctx, channel=channel)

    @_music.command(name="loop", aliases=["lp"])
    async def _loop(self, ctx: Context, mode: str):
        """반복 재생"""
        await play_loop(this=self, ctx=ctx, mode=mode)

    @_music.command(name="play", aliases=["music", "p"])
    async def play_(self, ctx: Context, *, search: str):
        """재생"""
        await play_music(this=self, ctx=ctx, search=search)

    @_music.command(name="play_list", aliases=["ml"])
    async def create_playlist_play(self, ctx: Context, *, search: str):
        """Youtube Playlist 재생"""
        await play_youtube_playlist(this=self, ctx=ctx, search=search)

    @_music.command(name="pause")
    async def pause_(self, ctx: Context):
        """일시중지"""
        await pause_play(this=self, ctx=ctx)

    @_music.command(name="resume")
    async def resume_(self, ctx: Context):
        """다시 재생"""
        await replay(this=self, ctx=ctx)

    @_music.command(name="skip")
    async def skip_(self, ctx: Context):
        """스킵"""
        await skip_song(ctx=ctx)

    @_music.command(name="remove", aliases=["rm"])
    async def _remove(self, ctx: Context, index: int):
        await remove_song(this=self, ctx=ctx, index=index)

    @_music.command(name="shuffle", aliases=["sff"])
    async def _shuffle(self, ctx: Context):
        await shuffle(this=self, ctx=ctx)

    @_music.command(name="queue", aliases=["q", "playlist"])
    async def queue_info(self, ctx: Context):
        """재생목록"""
        await get_playlist(this=self, ctx=ctx)

    @_music.command(
        name="now_playing", aliases=["np", "current", "playing"]
    )
    async def now_playing_(self, ctx: Context):
        """재생중인 컨텐츠 정보 보기"""
        await playing_song(this=self, ctx=ctx)

    @_music.command(name="volume", aliases=["vol"])
    async def change_volume(self, ctx: Context, *, vol: float):
        """사운드 크기 조절"""
        await change_player_volume(this=self, ctx=ctx, vol=vol)

    @_music.command(name="stop")
    async def stop_(self, ctx: Context):
        """stop"""
        await play_stop(this=self, ctx=ctx)


@Logger.set()
def setup(bot: Bot):
    bot.add_cog(Music(bot))