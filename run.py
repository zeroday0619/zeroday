import discord
from itertools import cycle
from discord.ext import tasks
from app.controller import bot


presence_message = ["!help", "Ver 3.5"]
extension_list = ["cogs.utils", "cogs.music", "cogs.system"]

presence = cycle(presence_message)


@tasks.loop(seconds=10)
async def change_status():
    await bot.change_presence(
        status=discord.Status.online, activity=discord.Game(next(presence))
    )


@bot.event
async def on_ready():
    print(
        "-------------------------------------------------------------------------------"
    )
    print(f"[*] Logged is as [{bot.user.name}]")
    print(f"[*] CID: {str(bot.user.id)}")
    print(f"[*] zeroday0619 | Copyright (C) 2020 zeroday0619")
    print(
        "-------------------------------------------------------------------------------"
    )
    print(f'[*] Completed! running the "zeroday" framework')
    await change_status.start()


bot.remove_command("help")
bot.load_extensions(extension_list)
bot.launch()
