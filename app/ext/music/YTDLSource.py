import re
import aiohttp
import discord
import asyncio
import youtube_dl

from discord import PCMVolumeTransformer
from discord.ext.commands import Context
from youtube_dl import YoutubeDL
from functools import partial
from app.module.spotify_to_youtube import SpotifyConverter
from app.ext.performance import run_in_threadpool
from app.ext.music.option import ytdl_format_options
from validator_collection import checkers
from app.ext.music.option import EmbedSaftySearch
from app.ext.music.option import adult_filter
from app.module import RegexFilter
from app.controller.logger import Logger

youtube_dl.utils.bug_reports_message = lambda: ""
ytdl = YoutubeDL(ytdl_format_options)

logger = Logger.generate_log()


@Logger.set(logger=logger)
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
    @Logger.set(logger=logger)
    async def _next_g(cls, ctx, text, block_text, i):
        cls.logger.info(f"Check: {i}")
        if bool(re.fullmatch(text.strip(), block_text[i])):
            try:
                embed_two = EmbedSaftySearch(data=str(text.strip()))
                await ctx.send(embed=embed_two)
            except Exception as e:
                cls.logger.debug(msg=e)
            return True


    @classmethod
    @Logger.set(logger=logger)
    async def naver_filter(cls, ctx, search_source: str):
        for text in list(cleanText(search_source).split()):
            if await adult_filter(search=str(text.strip()), loop=ctx.bot.loop) == 1:
                cls.logger.info(f"차단: {text.strip()}")
                try:
                    embed_two = EmbedSaftySearch(data=str(text.strip()))
                    await ctx.send(embed=embed_two)
                except Exception as e:
                    cls.logger.debug(msg=e)
                    pass
                return True
        return False

    @classmethod
    @Logger.set(logger=logger)
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

    @classmethod
    async def playlist_px(cls, ctx: Context, msg, data):
        try:
            if msg:
                await ctx.send(f"**{data['title']}**가 재생목록에 추가되었습니다.", delete_after=15, )
            return cls(discord.FFmpegPCMAudio(data["url"], **cls.FFMPEG_OPTIONS), data=data, requester=ctx.author, )
        except Exception as e:
            cls.logger.debug(msg=e)
            pass

    @classmethod
    @Logger.set(logger=logger)
    async def create_playlist(cls, ctx, search: str, *, download=False, msg=True, loop: asyncio.BaseEventLoop = None):
        try:
            loop = loop or asyncio.get_event_loop()
            data = await run_in_threadpool(lambda: ytdl.extract_info(url=search, download=download))
            return [await cls.playlist_px(ctx=ctx, msg=msg, data=ixc) for ixc in data["entries"]]
        except Exception as e:
            cls.logger.debug(msg=e, exc_info=True, stack_info=True)
            pass

    @classmethod
    @Logger.set(logger=logger)
    async def Search(cls, ctx, search: str, *, download=False, msg=True, loop: asyncio.BaseEventLoop = None):
        try:
            if not checkers.is_url(search):
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

            if await cls.naver_filter(ctx=ctx, search_source=data['title']):
                cls.logger.info(f"Detected: {data['title']}")
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
        except Exception as e:
            cls.logger.debug(msg=e)
            pass

    @classmethod
    @Logger.set(logger=logger)
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
    @Logger.set(logger=logger)
    def parse_duration(duration: int):
        try:
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
        except Exception as e:
            Logger.generate_log().debug(msg=e)
            return "ERROR"
