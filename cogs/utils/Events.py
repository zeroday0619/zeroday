import discord
import time
import datetime
from discord.ext import commands
from discord.ext.commands import Context, Bot
from app.controller.logger import Logger


class Events(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.logger = Logger.generate_log()

    @staticmethod
    async def error_binder(ctx: Context, error, exception, title: str, description: str):
        if isinstance(error, exception):
            err = discord.Embed(
                title=title,
                description=description,
            )
            return await ctx.send(embed=err, delete_after=5)

    @commands.Cog.listener()
    async def on_command_error(self, ctx: Context, error):
        """
        await self.error_binder(
            ctx=ctx,
            error=error,
            exception=commands.ExtensionError,
            title="Extension Error",
            description=error
        )
        """
        await self.error_binder(
            ctx=ctx,
            error=error,
            exception=commands.BotMissingPermissions,
            title="Bot Missing Permissions",
            description=error
        )