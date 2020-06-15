from discord.ext import commands
from discord.ext.commands import Cog
from discord.ext.commands import Bot


class Status(Cog):
    """상태정보"""
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.command(name='status', aliases=['ping', '핑'])
    async def ping(self, ctx):
        await ctx.send(
            f"Pong!"
        )