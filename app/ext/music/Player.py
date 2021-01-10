import asyncio
import discord
import random
import itertools

from async_timeout import timeout
from discord.ext.commands import Context
from discord import Guild
from .YTDLSource import YTDLSource
from app.controller.logger import Logger


class SongQueue(asyncio.Queue):
    _queue: list

    def __getitem__(self, item):
        if isinstance(item, slice):
            return list(itertools.islice(self._queue, item.start, item.stop, item.step))
        else:
            return self._queue[item]

    def __iter__(self):
        return self._queue.__iter__()

    def __len__(self):
        return self.qsize()

    def clear(self):
        self._queue.clear()

    def shuffle(self):
        random.shuffle(self._queue)

    def remove(self, index: int):
        del self._queue[index]


class Player:
    """Base class for Music Player"""
    __slots__ = (
        "bot",
        "_guild",
        "_channel",
        "_cog",
        "queue",
        "next",
        "current",
        "np",
        "repeat",
        "_volume",
        "_loop",
        "logger"
    )

    def __init__(self, ctx: Context):
        self.logger = Logger.generate_log()
        self.bot = ctx.bot
        self._guild: Guild = ctx.guild
        self._channel = ctx.channel
        self._cog = ctx.cog

        self.queue = SongQueue()
        self.next = asyncio.Event()
        self._volume = 0.5

        self.np = None
        self.current = None
        self._loop = False
        ctx.bot.loop.create_task(self.player_loop())

    @property
    def loop(self):
        return self._loop

    @loop.setter
    def loop(self, value: bool):
        self._loop = value

    @property
    def volume(self):
        return self._volume

    @volume.setter
    def volume(self, volume: float):
        self._volume = volume

    @property
    def is_playing(self):
        return self.np and self.current

    @staticmethod
    @Logger.set()
    async def create_embed(source, duration, requester, current, thumbnail):
        embed = (
            discord.Embed(
                title="Now playing",
                description="```css\n{0.title}\n```".format(source),
                color=discord.Color.blurple(),
            )
                .add_field(name="Duration", value=duration)
                .add_field(name="Requested by", value=requester)
                .add_field(
                name="Uploader",
                value="[{0.uploader}]({0.uploader_url})".format(current),
            )
                .add_field(
                name="URL", value="[Click]({0.web_url})".format(current)
            )
                .set_thumbnail(url=thumbnail)
        )
        return embed

    async def text_to_speech_loop(self, source):
        self._guild.voice_client.play(source)

    @Logger.set()
    async def player_loop(self):
        await self.bot.wait_until_ready()
        while not self.bot.is_closed():
            self.next.clear()

            try:
                async with timeout(300):  # 5 minutes
                    source = await self.queue.get()
            except asyncio.TimeoutError:
                if self in self._cog.players.values():
                    return self.destroy(self._guild)
                return

            source.volume = self.volume
            self.current = source
            if self._guild.voice_client is not None:
                self._guild.voice_client.play(
                    source,
                    after=lambda _: self.bot.loop.call_soon_threadsafe(self.next.set),
                )

            embed = await self.create_embed(
                source=source,
                duration=self.current.duration,
                requester=self.current.requester,
                current=self.current,
                thumbnail=self.current.thumbnail
            )

            self.np = await self._channel.send(
                embed=embed
            )

            await self.next.wait()
            if self.loop:
                ctx = await self.bot.get_context(self.np)
                ctx.author = source.requester
                search = source.web_url

                try:
                    source_repeat = await YTDLSource.Search(
                        ctx, search, download=False, msg=False
                    )
                except Exception as e:
                    self.logger.error(f"There was an error processing your song. {e}")
                    await self._channel.send(
                        f"There was an error processing your song.\n ```css\n[{e}]\n```"
                    )
                    continue

                if self.loop:
                    self.queue._queue.appendleft(source_repeat)
                else:
                    await self.queue.put(source_repeat)

            try:
                if not self.is_playing:
                    await self.np.delete()
            except discord.HTTPException:
                pass

    @Logger.set()
    async def stop(self):
        self.queue.clear()
        if self.np:
            await self._guild.voice_client.disconnect()
            self.np = None

    @Logger.set()
    def destroy(self, guild):
        # Disconnect and Cleanup
        return self.bot.loop.create_task(self._cog.cleanup(guild))
