from typing import List
from discord.ext import commands
from discord.ext.commands import Context
from discord.ext.commands import Bot
from app.error import DISCORD_COG_RELOAD_FAILED
from app.controller.logger import Logger


class system(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.logger = Logger.generate_log()
        self.extension_list = [
            "cogs.utils",
            "cogs.music",
            "cogs.system",
            "extensions.minecraft",
            "extensions.tts"
        ]

    @Logger.set()
    async def reload_extensions(self, _cogs: List[str]):
        for cog in _cogs:
            try:
                self.bot.reload_extension(cog)
            except Exception as ex:
                raise DISCORD_COG_RELOAD_FAILED(extension=cog, msg=ex)

            self.logger.info(f"Successfully reloaded {cog}")
        self.logger.info("Reload complete.")

    @commands.command(name="reload", hidden=True)
    async def cogs_reload(self, ctx: Context):
        await self.reload_extensions(_cogs=self.extension_list)
        await ctx.send("Reload complete.")


def setup(bot: Bot):
    bot.add_cog(system(bot))
