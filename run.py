import discord
from itertools import cycle
from discord.ext import tasks
from app.controller import bot
from app.controller.logger import Logger

logger = Logger.generate_log()

presence_message = ["!help", "Ver 3.5"]
extension_list = ["cogs.utils", "cogs.music", "cogs.system", "extensions.minecraft", "extensions.tts"]

presence = cycle(presence_message)


@tasks.loop(seconds=10)
async def change_status():
    await bot.change_presence(
        status=discord.Status.online, activity=discord.Game(next(presence))
    )


@Logger.set()
@bot.event
async def on_ready():
    logger.info("------------------------------------------------------------")
    logger.info(f"[*] Logged is as [{bot.user.name}]")
    logger.info(f"[*] CID: {str(bot.user.id)}")
    logger.info(f"[*] zeroday0619 | Copyright (C) 2021 zeroday0619")
    logger.info("------------------------------------------------------------")
    logger.info(f'[*] Completed!')
    await change_status.start()


bot.remove_command("help")
bot.load_extensions(extension_list)
bot.launch()
