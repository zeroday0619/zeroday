from typing import List
from discord.ext.commands import Bot
from app.controller.logger import Logger

from app.error import DISCORD_TOKEN_NOT_FOUND
from app.error import DISCORD_COG_LOAD_FAILED
from app.error import DISCORD_COG_RELOAD_FAILED


class Core(Bot):
    def __init__(self, discord_token: str, command_prefix: str, description: str, case_insensitive: bool):
        self.logger = Logger.generate_log()
        if not discord_token:
            raise DISCORD_TOKEN_NOT_FOUND

        self.d_token = discord_token
        super(Core, self).__init__(
            command_prefix=command_prefix,
            description=description,
            case_insensitive=case_insensitive
        )

    @Logger.set()
    def load_extensions(self, _cogs: List[str]):
        for extension in _cogs:
            try:
                self.load_extension(extension)
                self.logger.info(msg=f"Successfully loaded {extension}")
            except Exception as ex:
                raise DISCORD_COG_LOAD_FAILED(extension=extension, msg=ex)

    @Logger.set()
    def reload_extensions(self, _cogs: List[str]):
        for extension in _cogs:
            try:
                self.reload_extension(extension)
                self.logger.info(msg=f"Successfully reloaded {extension}")
            except Exception as ex:
                raise DISCORD_COG_RELOAD_FAILED(extension=extension, msg=ex)

    @Logger.set()
    def launch(self):
        self.run(self.d_token)
