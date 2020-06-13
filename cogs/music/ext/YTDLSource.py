import discord
import asyncio
import youtube_dl
import functools
import itertools

from core import bot
from .option import EmbedSaftySearch
from .option import adult_filter
from .option import BlockedContent

from discord import FFmpegPCMAudio
from discord import PCMVolumeTransformer

from discord.ext import commands
from discord.ext.commands import Bot
from discord.ext.commands import Cog
from discord.ext.commands import Context
from discord.ext.commands import CommandError
from pathlib import Path

from asyncio import BaseEventLoop
from youtube_dl import YoutubeDL

from .option import ffmpeg_options, ffmpeg_options_a
from .option import ytdl_format_options
from .performance import run_in_threadpool

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
    async def create_playlist(cls, ctx, search: str, *, loop, download=True):
        loop = loop or asyncio.get_event_loop()
        data = await ytdl.extract_info(url=search, download=download)

        songs = []
        for data in data['entries']:
            await ctx.send("**{}**가 재생목록에 추가되었습니다.".format(str(data['title'])), delete_after=5)

            if download:
                source = ytdl.prepare_filename(data)
                songs.append(cls(discord.FFmpegPCMAudio(source), data=data, requester=ctx.author))
            else:
                songs.append({'webpage_url': data['webpage_url'], 'requester': ctx.author, 'title': data['title']})
        return songs

    @classmethod
    async def Search(cls, ctx, search: str, *, loop, download=False, msg=True):
        loop = loop or asyncio.get_event_loop()
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
        else:
            return {'webpage_url': data['webpage_url'], 'requester': ctx.author, 'title': data['title']}

        return cls(discord.FFmpegPCMAudio(source=source, executable="ffmpeg", options="-async 1 -ab 720k -vcodec flac -threads 16"), data=data, requester=ctx.author)

    @classmethod
    async def regather_stream(cls, data, *, loop):
        loop = loop or asyncio.get_event_loop()
        requester = data['requester']

        data = await run_in_threadpool(lambda: ytdl.extract_info(url=data['webpage_url'], download=False))

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
