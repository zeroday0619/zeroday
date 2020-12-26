import asyncio
import discord
import random
import itertools
from async_timeout import timeout
from .YTDLSource import YTDLSource


class SongQueue(asyncio.Queue):
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
        "volume",
        "repeat",
    )

    def __init__(self, ctx):
        self.bot = ctx.bot
        self._guild = ctx.guild
        self._channel = ctx.channel
        self._cog = ctx.cog

        self.queue = SongQueue()
        self.next = asyncio.Event()

        self.np = None
        self.volume = 0.5
        self.current = None
        self.repeat = False
        ctx.bot.loop.create_task(self.player_loop())

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
            print(self.current.thumbnail)

            embed = (
                discord.Embed(
                    title="Now playing",
                    description="```css\n{0.title}\n```".format(source),
                    color=discord.Color.blurple(),
                )
                    .add_field(name="Duration", value=self.current.duration)
                    .add_field(name="Requested by", value=self.current.requester)
                    .add_field(
                    name="Uploader",
                    value="[{0.uploader}]({0.uploader_url})".format(self.current),
                )
                    .add_field(
                    name="URL", value="[Click]({0.web_url})".format(self.current)
                )
                    .set_thumbnail(url=self.current.thumbnail)
            )
            print(source)
            self._guild.voice_client.play(
                source,
                after=lambda _: self.bot.loop.call_soon_threadsafe(self.next.set),
            )
            self.np = await self._channel.send(embed=embed)

            await self.next.wait()

            if self.repeat:
                ctx = await self.bot.get_context(self.np)
                ctx.author = source.requester
                search = source.web_url

                try:
                    source_repeat = await YTDLSource.Search(
                        ctx, search, download=False, msg=False
                    )
                except Exception as e:
                    await self._channel.send(
                        f"There was an error procecsing your song.\n ```css\n[{e}]\n```"
                    )
                    continue

                if self.repeat == "current":
                    self.queue._queue.appendleft(source_repeat)
                else:
                    await self.queue.put(source_repeat)

            try:
                await self.np.delete()
            except discord.HTTPException:
                pass

    def destroy(self, guild):
        # Disconnect and Cleanup
        return self.bot.loop.create_task(self._cog.cleanup(guild))
