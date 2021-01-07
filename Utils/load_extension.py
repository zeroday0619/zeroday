from app.controller import bot
from typing import List


def load_extension(_cogs: List[str]):
    for extension in _cogs:
        try:
            bot.load_extension(extension)
            print(f"Successfully loaded {extension}")
        except Exception as ex:
            print(f"Failed to load extension {extension}: {ex}")


def reload_extension(_cogs: List[str]):
    for extension in _cogs:
        try:
            bot.reload_extension(extension)
            print(f"Successfully reloaded {extension}")
        except Exception as ex:
            print(f"Failed to reload extension {extension}: {ex}")
