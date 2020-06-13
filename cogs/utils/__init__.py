from discord.ext.commands import Bot
from .CTF import CTF
from .Events import Events
from .Status import Status
from .zeroday import zeroday

def setup(bot: Bot):
    bot.remove_command("help")
    bot.add_cog(zeroday(bot))
    bot.add_cog(Status(bot))
    bot.add_cog(Events(bot))
    bot.add_cog(CTF(bot))