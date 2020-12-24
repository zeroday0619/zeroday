import discord
from discord.ext import commands
from app.ext.music.filter import safe


class VoiceConnectionError(commands.CommandError):
    """Custom Exception class for connection errors."""


class InvalidVoiceChannel(VoiceConnectionError):
    """Exception for cases of invalid Voice Channels."""


def ytdl_format_options_a():
    options = {
        "format": "bestaudio/best",
        "outtmpl": "downloads/%(extractor)s-%(id)s-%(title)s.%(ext)s",
        "restrictfilenames": True,
        "noplaylist": True,
        "nocheckcertificate": True,
        "ignoreerrors": False,
        "logtostderr": False,
        "quiet": True,
        "no_warnings": True,
        "default_search": "auto",
        "source_address": "0.0.0.0",
        "age-limit": 17
    }
    return options


# -reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5
# -reconnect 1 -reconnect_at_eof 1 -reconnect_streamed 1 -reconnect_delay_max 5
def ffmpeg_options_a():
    options = {"before_options": "-nostdin", "options": "-vn"}
    return options


ytdl_format_options = ytdl_format_options_a()
ffmpeg_options = ffmpeg_options_a()

embed_ERROR = discord.Embed(
    title="Music",
    description="```css\n재생하고있는 Music 이 없습니다.\n```",
    color=discord.Color.blurple(),
).add_field(name="INFO", value="stable")

embed_queued = discord.Embed(
    title="Music",
    description="```css\n현재 대기중인 노래가 더 이상 없습니다.\n```",
    color=discord.Color.blurple(),
).add_field(name="INFO", value="stable")
embed_value = discord.Embed(
    title="Music",
    description="```css\n1에서 100 사이의 값을 입력하십시오.\n```",
    color=discord.Color.blurple(),
).add_field(name="INFO", value="stable")


def EmbedSaftySearch(data):
    print(str(data))
    embed_saftyq = discord.Embed(
        title="불법·유해 미디어에 대한 차단 안내",
        url="http://warning.or.kr/",
        description=f"```ini\n어허 그러면 안 돼~```",
        color=discord.Color.blurple(),
    ).set_image(
        url="https://media.tenor.co/videos/2bd04907690989615a243b2c9f2aba40/mp4"
    ).add_field(
        name="Blocked words", value=str(data.strip()), inline=False
    ).set_footer(
        text="Safe Search | Version: alpha 1.0.0", icon_url="https://cdn.imgbin.com/23/8/2/imgbin-google-safe-browsing-web-browser-malware-safe-yPAFE8aZ6VYPygxttJYmr5qkS.jpg"
    )
    return embed_saftyq


class BlockedContent(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


async def adult_filter(search, loop):
    if await safe.adult_filter(search=str(search), loop=loop) == 1:
        return 1
    elif await safe.adult_filter(search=str(search), loop=loop) == 2:
        return 1
    else:
        return 0
