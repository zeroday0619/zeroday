from core import *
from typing import List


def LoadExtension(_cogs: List[str]):
    for extension in _cogs:
        try:
            bot.load_extension(extension)
            print(f"Successfully loaded {extension}")
        except Exception as ex:
            print(f"Failed to load extension {extension}: {ex}")


def ReloadExtension(_cogs: List[str]):
    for extension in _cogs:
        try:
            bot.reload_extension(extension)
            print(f"Successfully reloaded {extension}")
        except Exception as ex:
            print(f"Failed to reload extension {extension}: {ex}")


def AsyncLoadExtension(_cogs: List[str]):
    for extension in _cogs:
        try:
            bot.loop.run_in_executor(None, bot.load_extension, extension)
            print(f"Successfully loaded {extension}")
        except Exception as ex:
            print(f"Failed to load extension {extension}: {ex}")
