import discord
import time
import datetime
from discord.ext import commands
from app.controller.logger import Logger


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = Logger.generate_log()

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            CheckFailure = discord.Embed(
                title="Permission Error",
                description="You don't have the permissions to do that!",
            )
            await ctx.send(embed=CheckFailure, delete_after=5)
