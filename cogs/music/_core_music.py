import re
import asyncio
import discord
import itertools
from discord import Guild

from discord.ext import commands
from discord.ext.commands import Bot
from discord.ext.commands import Context
from discord.ext.commands import NoPrivateMessage
from validator_collection import checkers
from app.error.music import InvalidVoiceChannel
from app.ext.music.YTDLSource import YTDLSource
from app.ext.music.Player import Player
from app.controller.logger import Logger


__version__ = "3.5.0"


class CoreMusic(commands.Cog):
    """뮤직 모듈"""

    __slots__ = ("bot", "players", "logger", "status")

    def __init__(self, bot: Bot):
        self.logger = Logger.generate_log()
        self.status = False
        self.bot = bot
        self.players = {}
        self.cog_version = __version__
        self.ver_string = "Ver"

    @Logger.set()
    async def cleanup(self, guild: Guild):
        """
        :param guild: Represents a Discord guild.
        """
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
    async def __local_check(ctx: Context):
        if not ctx.guild:
            raise NoPrivateMessage
        return True

    @staticmethod
    @Logger.set()
    async def __error(ctx: Context, error):
        if isinstance(error, NoPrivateMessage):
            try:
                return await ctx.send("이 Command 는 DM 에서 사용할 수 없습니다")
            except discord.HTTPException as e:
                raise e

        elif isinstance(error, InvalidVoiceChannel):
            return await ctx.send(
                "Voice Channel 연결중 Error 가 발생하였습니다\n 자신이 Voice Channel에 접속되어 있는 지 확인 바랍니다."
            )

        Logger.generate_log().error("Ignoring exception in command {}".format(ctx.command))
        Logger.generate_log().exception(error)
        return await ctx.send("ERROR: Ignoring exception in command {}".format(ctx.command))

    @Logger.set()
    def get_player(self, ctx: Context):
        """
        :rtype: object
        """

        try:
            player = self.players[ctx.guild.id]
        except KeyError:
            player = Player(ctx)
            self.players[ctx.guild.id] = player
        return player

    @Logger.set()
    async def sleep(self, source):
        if self.status:
            return None

        await asyncio.sleep(3)
        return source

    @Logger.set()
    async def check(self, ctx: Context, search):
        try:
            print(self.status)
            if self.status:
                raise Exception

            if checkers.is_url(search):
                source = await YTDLSource.Search(ctx, search, download=False, loop=ctx.bot.loop)
                return source
            else:
                search_text = search
                serc = search_text.replace(":", "")
                source = await YTDLSource.Search(ctx, serc, download=False, loop=ctx.bot.loop)
                return source
        except Exception as e:
            Logger.generate_log().debug(msg=e)
            pass

    @Logger.set()
    async def pause_embed(self, ctx: Context):
        nx = discord.Embed(
            title="Music",
            description=f"```css\n{ctx.author} : 일시중지.\n```",
            color=discord.Color.blurple(),
        ).add_field(name=self.ver_string, value=self.cog_version)
        return nx

    @Logger.set()
    async def resume_embed(self, ctx: Context):
        nx = discord.Embed(
            title="Music",
            description=f"```css\n**{ctx.author}** : 다시재생.\n```",
            color=discord.Color.blurple(),
        ).add_field(name=self.ver_string, value=self.cog_version)
        return nx

    @Logger.set()
    async def volume_embed(self, ctx: Context, vol):
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

