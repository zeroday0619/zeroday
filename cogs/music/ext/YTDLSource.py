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
    FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
        'options': '-vn',
    }

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
    async def search_source(cls, ctx, search: str, *, download=False):
        channel = ctx.channel
        cls.search_query = '%s%s:%s' % ('ytsearch', 10, ''.join(search))
        info = await run_in_threadpool(lambda :ytdl.extract_info(cls.search_query, download=download, process=False))

        cls.search = {}
        cls.search['title'] = f'Search result for:\n**{search}**'
        cls.search['type'] = 'rich'
        cls.search['color'] = 7506394
        cls.search['author'] = {
            'name': f'{ctx.author.name}',
            'url': f'{ctx.author.avatar_url}',
            'icon_url': f'{ctx.author.avatar_url}'
        }

        lst = []

        for e in info['entries']:
            VId = e.get('id')
            VUrl = 'https://www.youtube.com/watch?v=%s' % (VId)
            lst.append(f'`{info["entries"].index(e) + 1}.` [{e.get("title")}]({VUrl})\n')

        lst.append('\n**Type a number to make a choice, Type `cancel` to exit**')
        cls.search["description"] = "\n".join(lst)

        em = discord.Embed.from_dict(cls.search)
        await ctx.send(embed=em, delete_after=45.0)

        def check(msg):
            return msg.content.isdigit() == True and msg.channel == channel or msg.content == 'cancel' or msg.content == 'Cancel'

        try:
            m = await ctx.bot.wait_for('message', check=check, timeout=45.0)

        except asyncio.TimeoutError:
            rtrn = 'timeout'

        else:
            if m.content.isdigit() == True:
                sel = int(m.content)
                print(sel)
                if 0 < sel <= 10:
                    for key, value in info.items():
                        if key == 'entries':
                            """data = value[sel - 1]"""
                            VId = value[sel - 1]['id']
                            VUrl = 'https://www.youtube.com/watch?v=%s' % (VId)
                            data = await run_in_threadpool(lambda : ytdl.extract_info(VUrl, download=False))
                    rtrn = cls(discord.FFmpegPCMAudio(data['url'], **cls.FFMPEG_OPTIONS), data=data, requester=ctx.author)
                else:
                    rtrn = 'sel_invalid'
            elif m.content == 'cancel':
                rtrn = 'cancel'
            else:
                rtrn = 'sel_invalid'
        return rtrn

    @classmethod
    async def create_playlist(cls, ctx, search: str, *, download=True, msg=True):
        data = await run_in_threadpool(lambda: ytdl.extract_info(url=search, download=download))
        songs = []
        for data in data['entries']:
            if await adult_filter(search=str(data['title'])) == 1:
                embed_two = EmbedSaftySearch(data=str(data['title']))
                await ctx.send(embed=embed_two)
            else:
                if msg:
                    await ctx.send("**{}**가 재생목록에 추가되었습니다.".format(str(data['title'])), delete_after=15)

                if download:
                    source = await run_in_threadpool(lambda: ytdl.prepare_filename(data))
                    songs.append(cls(discord.FFmpegPCMAudio(source=source), data=data, requester=ctx.author))
                else:
                    songs.append(cls(discord.FFmpegPCMAudio(data['url'], **cls.FFMPEG_OPTIONS), data=data, requester=ctx.author))
        return songs

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
        else:
            return cls(discord.FFmpegPCMAudio(data['url'], **cls.FFMPEG_OPTIONS), data=data, requester=ctx.author)

        return cls(discord.FFmpegPCMAudio(source=source, executable="ffmpeg", options="-async 1 -ab 720k -vcodec flac -threads 16"), data=data, requester=ctx.author)

    @classmethod
    async def regather_stream(cls, ctx, *, download=False):
        data = await run_in_threadpool(lambda : ytdl.extract_info(url=data['webpage_url'], download=download))
        return cls(discord.FFmpegPCMAudio(data['url'], **cls.FFMPEG_OPTIONS), data=data, requester=ctx.author)

    @staticmethod
    def parse_duration(duration: int):
        if duration > 0:
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
            
            value = ', '.join(duration)
        
        elif duration == 0:
            value = "LIVE BATA"
        
        return value
