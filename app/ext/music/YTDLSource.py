import re
import aiohttp
import discord
import asyncio
import youtube_dl

from discord import PCMVolumeTransformer
from discord.ext.commands import Context
from youtube_dl import YoutubeDL
from functools import partial

from app.ext.performance import run_in_threadpool
from app.ext.music.option import ytdl_format_options
from validator_collection import checkers
from app.ext.music.option import EmbedSaftySearch
from app.ext.music.option import adult_filter
from app.module import RegexFilter
from app.controller.logger import Logger


youtube_dl.utils.bug_reports_message = lambda: ""
ytdl = YoutubeDL(ytdl_format_options)


@Logger.set()
def cleanText(readData):
    text = re.sub('[-=+,#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\'…》]', '', readData)
    return text


class YTDLSource(PCMVolumeTransformer):
    logger = Logger.generate_log()
    FFMPEG_OPTIONS = {
        "before_options": "-reconnect 1 -reconnect_at_eof 1 -reconnect_streamed 1 -reconnect_delay_max 5",
        "options": "-vn",
    }

    def __init__(self, source, *, data, requester):

        super().__init__(source)
        self.logger = Logger.generate_log()
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
    @Logger.set()
    async def LoadASTI_DB(cls, ctx) -> list:
        async with aiohttp.ClientSession() as session:
            async with session.get(url="https://zeroday0619.github.io/ASTI_DB/src/db.json") as resp:
                if resp.status != 200:
                    await ctx.send("ASTI DB Connect Failed!")
                cls.logger.info(f"Connect ASTI database | status code : {resp.status}")
                nxg = await resp.json()
            block_text = nxg['word']
        return block_text

    @classmethod
    @Logger.set()
    async def _next_g(cls, ctx, text, block_text, i):
        cls.logger.info(f"Check: {i}")
        if bool(re.fullmatch(text.strip(), block_text[i])):
            embed_two = EmbedSaftySearch(data=str(text.strip()))
            await ctx.send(embed=embed_two)
            return True

    @classmethod
    @Logger.set()
    async def next_generation_filter(cls, ctx, search_source: str):
        block_text = await cls.LoadASTI_DB(ctx=ctx)
        for text in list(cleanText(search_source).split()):
            for i in range(0, len(block_text)):
                if await cls._next_g(ctx=ctx, text=text, block_text=block_text, i=i):
                    return True
        return False

    @classmethod
    @Logger.set()
    async def naver_filter(cls, ctx, search_source: str):
        for text in list(cleanText(search_source).split()):
            if await adult_filter(search=str(text.strip()), loop=ctx.bot.loop) == 1:
                cls.logger.info(f"차단: {text.strip()}")
                embed_two = EmbedSaftySearch(data=str(text.strip()))
                await ctx.send(embed=embed_two)
                return True
        return False
    
    @classmethod
    @Logger.set()
    async def regex_filter(cls, ctx: Context, source: str):
        tool = RegexFilter()
        if await tool.check(source=source):
            cls.logger.info(f"차단: {source}")
            embed = EmbedSaftySearch(data=str(source))
            await ctx.send(embed=embed)
            return True
        else:
            return False

    @classmethod
    async def playlist_px(cls, ctx: Context, msg, data):
        await cls.regex_filter(ctx, data["title"])
        if msg:
            await ctx.send(f"**{data['title']}**가 재생목록에 추가되었습니다.", delete_after=15,)
        return cls(discord.FFmpegPCMAudio(data["url"], **cls.FFMPEG_OPTIONS), data=data, requester=ctx.author,)

    @classmethod
    @Logger.set()
    async def create_playlist(cls, ctx, search: str, *, download=False, msg=True, loop: asyncio.BaseEventLoop = None):
        loop = loop or asyncio.get_event_loop()
        data = await run_in_threadpool(lambda: ytdl.extract_info(url=search, download=download))
        return [await cls.playlist_px(ctx=ctx, msg=msg, data=ixc) for ixc in data["entries"]]

    @classmethod
    @Logger.set()
    async def Search(cls, ctx, search: str, *, download=False, msg=True, loop: asyncio.BaseEventLoop = None):

        if not checkers.is_url(search):
            if await cls.next_generation_filter(ctx=ctx, search_source=search):
                cls.logger.info(f"Detected: {search}")
                return None

            if await cls.regex_filter(ctx=ctx, source=str(search)):
                cls.logger.info(f"Detected: {search}")
                return None

        loop = loop or asyncio.get_event_loop()
        params_data = partial(ytdl.extract_info, url=str(search), download=download)
        data = await loop.run_in_executor(None, params_data)

        if "entries" in data:
            data = data["entries"][0]

        if await cls.regex_filter(ctx=ctx, source=data['title']):
            cls.logger.info(f"Detected: {data['title']}")
            return None

        if await cls.next_generation_filter(ctx=ctx, search_source=data['title']):
            cls.logger.info(f"Detected: {data['title']}")
            return None

        if await cls.naver_filter(ctx=ctx, search_source=data['title']):
            cls.logger.info(f"Detected: {data['title']}")
            return None

        if await adult_filter(search=str(cleanText(data["title"])), loop=ctx.bot.loop) == 1:
            cls.logger.info(f"차단: {data['title']}")
            embed_two = EmbedSaftySearch(data=str(data["title"]))
            await ctx.send(embed=embed_two)
            return None

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
    @Logger.set()
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
    @Logger.set()
    def parse_duration(duration: int):
        value = None
        if duration > 0:
            minutes, seconds = divmod(duration, 60)
            hours, minutes = divmod(minutes, 60)
            days, hours = divmod(hours, 24)

            duration = []
            _duration = duration.append
            if days > 0:
                _duration(f"{days} days")
            if hours > 0:
                _duration(f"{hours} hours")
            if minutes > 0:
                _duration(f"{minutes} minutes")
            if seconds > 0:
                _duration(f"{seconds} seconds")

            value = ", ".join(duration)

        elif duration == 0:
            value = "LIVE STREAM"
        return value
