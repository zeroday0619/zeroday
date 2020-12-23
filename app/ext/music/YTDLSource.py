import re
import discord
import asyncio
import youtube_dl

from discord import PCMVolumeTransformer
from youtube_dl import YoutubeDL
from functools import partial

from app.ext.performance import run_in_threadpool
from app.ext.music.option import ytdl_format_options
from app.ext.music.option import EmbedSaftySearch
from app.ext.music.option import adult_filter

youtube_dl.utils.bug_reports_message = lambda: ""
ytdl = YoutubeDL(ytdl_format_options)


class YTDLSource(PCMVolumeTransformer):
    FFMPEG_OPTIONS = {
        "before_options": "-reconnect 1 -reconnect_at_eof 1 -reconnect_streamed 1 -reconnect_delay_max 5",
        "options": "-vn",
    }

    def __init__(self, source, *, data, requester):
        super().__init__(source)
        self.requester = requester
        self.filename = ytdl.prepare_filename(data)
        date = data.get("upload_date")
        self.url = data.get("url")  # Youtube Addresses
        self.web_url = data.get("webpage_url")
        self.data = data  # Youtube Content Data
        self.title = data.get("title")  # Youtube Title
        self.thumbnail = data.get("thumbnail")  # Youtube Thumbnail
        self.uploader = data.get("uploader")  # Youtube Uploader
        self.uploader_url = data.get("uploader_url")
        self.description = data.get("description")

        self.duration = self.parse_duration(int(data.get("duration")))

    def __getitem__(self, item: str):
        return self.__getattribute__(item)

    @classmethod
    async def create_playlist(cls, ctx, search: str, *, download=False, msg=True, loop: asyncio.BaseEventLoop = None):
        loop = loop or asyncio.get_event_loop()
        params_data = partial(ytdl.extract_info, url=search, download=download)
        data = await loop.run_in_executor(None, params_data)

        songs = []
        song = songs.append
        for data in data["entries"]:
            if msg:
                await ctx.send(
                    "**{}**가 재생목록에 추가되었습니다.".format(str(data["title"])),
                    delete_after=15,
                )

            song(
                cls(
                    discord.FFmpegPCMAudio(data["url"], **cls.FFMPEG_OPTIONS),
                    data=data,
                    requester=ctx.author,
                )
            )
        return songs

    @classmethod
    async def Search(cls, ctx, search: str, *, download=False, msg=True, loop: asyncio.BaseEventLoop = None):

        block_text = ["빌리와구슬고자", "sex", "shitass", "asshole"]

        for text in list(search.split(" ")):
            for i in range(0, len(block_text)):
                print(f"A Check: {i}")
                if bool(re.search(text.strip(), block_text[i])):
                    print("차단 A")
                    embed_two = EmbedSaftySearch(data=str(text.strip()))
                    await ctx.send(embed=embed_two)
                    return None

            print("pass")

        loop = loop or asyncio.get_event_loop()
        params_data = partial(ytdl.extract_info, url=str(search), download=download)
        data = await loop.run_in_executor(None, params_data)

        if "entries" in data:
            data = data["entries"][0]

        for text in list(data["title"].split(" ")):
            for i in range(0, len(block_text)):
                print(f"B Check: {i}")
                if bool(re.fullmatch(text.strip(), block_text[i])):
                    print("차단 B")
                    embed_two = EmbedSaftySearch(data=str(text.strip()))
                    await ctx.send(embed=embed_two)
                    return None

        for text in list(data['title'].split(" ")):
            print(text)
            if await adult_filter(search=str(text.strip()), loop=ctx.bot.loop) == 1:
                print("차단 E")
                embed_two = EmbedSaftySearch(data=str(data["title"]))
                await ctx.send(embed=embed_two)
                return None

        if await adult_filter(search=str(data["title"]), loop=ctx.bot.loop) == 1:
            print("차단 F")
            embed_two = EmbedSaftySearch(data=str(data["title"]))
            await ctx.send(embed=embed_two)

        if msg:
            await ctx.send(
                "**{}**가 재생목록에 추가되었습니다.".format(str(data["title"])), delete_after=5
            )

        # =============================================================================================
        return cls(
            discord.FFmpegPCMAudio(data["url"], **cls.FFMPEG_OPTIONS),
            data=data,
            requester=ctx.author,
        )

    @classmethod
    async def regather_stream(cls, ctx, *, download=False):
        data = await run_in_threadpool(
            lambda: ytdl.extract_info(url=data["webpage_url"], download=download)
        )
        return cls(
            discord.FFmpegPCMAudio(data["url"], **cls.FFMPEG_OPTIONS),
            data=data,
            requester=ctx.author,
        )

    @staticmethod
    def parse_duration(duration: int):
        value = None
        if duration > 0:
            minutes, seconds = divmod(duration, 60)
            hours, minutes = divmod(minutes, 60)
            days, hours = divmod(hours, 24)

            duration = []
            _duration = duration.append
            if days > 0:
                _duration("{} days".format(days))
            if hours > 0:
                _duration("{} hours".format(hours))
            if minutes > 0:
                _duration("{} minutes".format(minutes))
            if seconds > 0:
                _duration("{} seconds".format(seconds))

            value = ", ".join(duration)

        elif duration == 0:
            value = "LIVE BETA"
        return value
