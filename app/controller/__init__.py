import json
from app.service import Core
from discord.ext import commands

with open("config.json", "r", encoding="utf-8") as _config:
    config: dict = json.load(_config)

discord_token = config['Token']
d_command_prefix: str = config['command_prefix']
d_description = config['description']
kakao_rest_api_key = config["kakao"]["REST_API_KEY"]
spotify_credentials: dict = config['spotify']

bot = Core(
    discord_token=discord_token,
    command_prefix=commands.when_mentioned_or(d_command_prefix),
    description=d_description,
    case_insensitive=True
)
