import discord
import asyncio
import youtube_dl

from discord import PCMVolumeTransformer
from youtube_dl import YoutubeDL
from functools import partial

from .performance import run_in_threadpool
from .option import ytdl_format_options
from .option import EmbedSaftySearch
from .option import adult_filter


youtube_dl.utils.bug_reports_message = lambda: ''
ytdl = YoutubeDL(ytdl_format_options)


class YTDLSource(PCMVolumeTransformer):
    def __init__(self, source, *, data, requester):
        super().__init__(source)
        self.requester = requester
        self.filename = ytdl.prepare_filename(data)
        date = data.get('upload_date')
        self.url = data.get('url')  # Youtube Addresses
        self.web_url = data.get('webpage_url')
        self.data = data # Youtube Content Data
        self.title = data.get('title') # Youtube Title
        self.thumbnail = data.get('thumbnail') # Youtube Thumbnail
        self.uploader = data.get('uploader') # Youtube Uploader
        self.uploader_url = data.get('uploader_url')
        self.description = data.get('description')

        self.duration = self.parse_duration(int(data.get('duration')))
    
    def __getitem__(self, item: str):
        return self.__getattribute__(item)

    @classmethod
    async def Search(cls, ctx, search: str, *, download=False, msg=True):
        data = await run_in_threadpool(lambda: ytdl.extract_info(url=search, download=download))
        if 'entries' in data:
            data = data['entries'][0]

        if await adult_filter(search=str(data['title'])) == 1:
            embed_two = EmbedSaftySearch(data=str(data['title']))
            await ctx.send(embed=embed_two)
            return

        if msg:
            await ctx.send("**{}**가 재생목록에 추가되었습니다.".format(str(data['title'])), delete_after=5)

        # =============================================================================================
        if download:
            source = await run_in_threadpool(lambda: ytdl.prepare_filename(data))
            print(source)
        else:
            return {'webpage_url': data['webpage_url'], 'requester': ctx.author, 'title': data['title']}

        return cls(discord.FFmpegPCMAudio(source=source, executable="ffmpeg", options="-async 1 -ab 720k -vcodec flac -threads 16"), data=data, requester=ctx.author)

    @classmethod
    async def regather_stream(cls, data, *, loop):
        loop = loop or asyncio.get_event_loop()
        requester = data['requester']

        to_run = partial(ytdl.extract_info, url=data['webpage_url'], download=False)
        data = await loop.run_in_executor(None, to_run)

        return cls(discord.FFmpegPCMAudio(data['url']), data=data, requester=requester)

    @staticmethod
    def parse_duration(duration: int):
        minutes, seconds = divmod(duration, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)

        duration = []
        if days > 0:
            duration.append('{} days'.format(days))
        if hours > 0:
            duration.append('{} hours'.format(hours))
        if minutes > 0:
            duration.append('{} minutes'.format(minutes))
        if seconds > 0:
            duration.append('{} seconds'.format(seconds))
        return ', '.join(duration)
