from core import *
from Utils.load_extension import LoadExtension as sync_add_extension
from Utils.load_extension import AsyncLoadExtension as async_add_extension
from Utils.discord_presense_task import change_status

token = config["Token"]

_ext_1 = ["cogs.utils", "cogs.music"]
_ext_2 = ["Utils.discord_presense_task"]


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
async_add_extension(_cogs=_ext_1)
sync_add_extension(_cogs=_ext_2)
bot.run(token)