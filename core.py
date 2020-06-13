from discord.ext.commands import AutoShardedBot
from Utils import config
from itertools import cycle

status = cycle(
    [        
        '!help',
        '20200612 RC 1347'
    ]
)


class Bot(AutoShardedBot):
    def __init__(self, *args, prefix=None, **kwargs):
        super().__init__(*args, **kwargs)


bot = Bot(command_prefix=config['command_prefix'], description=config['description'])