from typing import List
from discord.ext.commands import Bot
from app.error import DISCORD_TOKEN_NOT_FOUND


class Core(Bot):
    def __init__(self, discord_token: str, command_prefix: str, description: str, case_insensitive: bool):
        if not discord_token:
            raise DISCORD_TOKEN_NOT_FOUND

        self.d_token = discord_token
        super(Core, self).__init__(
            command_prefix=command_prefix,
            description=description,
            case_insensitive=case_insensitive
        )

    def load_extensions(self, _cogs: List[str]):
        for extension in _cogs:
            try:
                self.load_extension(extension)
                print(f"Successfully loaded {extension}")
            except Exception as ex:
                print(f"Failed to load extension {extension}: {ex}")

    def reload_extensions(self, _cogs: List[str]):
        for extension in _cogs:
            try:
                self.reload_extension(extension)
                print(f"Successfully reloaded {extension}")
            except Exception as ex:
                print(f"Failed to reload extension {extension}: {ex}")

    def launch(self):
        self.run(self.d_token)
