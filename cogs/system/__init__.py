from discord.ext import commands
from discord.ext.commands import Bot


class system(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.command(name="reload", hidden=True)
    async def cogs_reload(self, ctx):
        try:
            self.bot.unload_extension("cogs.music")
            self.bot.load_extension("cogs.music")
            print("-----------------------------------------")
            self.bot.unload_extension("cogs.utils")
            self.bot.load_extension("cogs.utils")
        except Exception as e:
            await ctx.send(f"**`ERROR:`** {type(e).__name__} - {e}")
        else:
            await ctx.send("**`SUCCESS`**")


def setup(bot: Bot):
    bot.add_cog(system(bot))
