from discord.ext.commands import Bot
from Utils import config
from itertools import cycle

status = cycle(["!help", "Ver 3.1"])


class Bot(Bot):
    def __init__(self, *args, prefix=None, **kwargs):
        super().__init__(*args, **kwargs)


bot = Bot(
    command_prefix=config["command_prefix"],
    description=config["description"],
    case_insensitive=True,
)
