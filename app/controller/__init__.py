import json
from app.service import Core


with open("config.json", "r", encoding="utf-8") as _config:
    config: dict = json.load(_config)

discord_token = config['Token']
d_command_prefix = config['command_prefix']
d_description = config['description']

bot = Core(
    discord_token=discord_token,
    command_prefix=d_command_prefix,
    description=d_description,
    case_insensitive=True
)