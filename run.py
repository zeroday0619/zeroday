from Utils.discord_presense_task import change_status
from Utils.load_extension import LoadExtension, ReloadExtension, AsyncLoadExtension
from core import *
import nest_asyncio
import uvloop

nest_asyncio.apply()

token = config['Token']


async_ext = ["cogs.utils", "cogs.music"]
_ext = ["Utils.discord_presense_task"]
reload_ext = ["cogs.utils", "cogs.music", "Utils.discord_presense_task"]


@bot.event
async def on_ready():
    print("-------------------------------------------------------------------------------")
    print(f'[*] Logged is as [{bot.user.name}]')
    print(f'[*] CID: {str(bot.user.id)}')
    print(f'[*] zeroday0619 | Copyright (C) 2020 zeroday0619')
    print("-------------------------------------------------------------------------------")
    print(f'[*] Completed! running the "zeroday" framework')
    await change_status.start()

if __name__ == '__main__':
    try:
        bot.loop.run_in_executor(None, bot.remove_command, "help")
        AsyncLoadExtension(_cogs=async_ext)
        LoadExtension(_cogs=_ext)
        uvloop.loop.Loop.run_until_complete(bot.run(token))
    except TypeError:
        print("\nShutdown SUCCESS!")
    except RuntimeError:
        print("RUNTIME ERROR..... Reload Extension!")
        try:
            ReloadExtension(_cogs=reload_ext)
        except Exception as ex:
            print(f"SYSTEM ERROR: {ex}")