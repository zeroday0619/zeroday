import discord
import time
import datetime
from discord.ext import commands


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")
        user = message.author
        msg = message.content
        print(f"<{st}> : [{user}] >> {msg}")

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            CheckFailure = discord.Embed(
                title="Permission Error",
                description="You don't have the permissions to do that!",
            )
            await ctx.send(embed=CheckFailure, delete_after=5)
