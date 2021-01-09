import os
import psutil
import discord
import platform

from discord.ext import commands
from discord.ext.commands import Cog
from discord.ext.commands import Bot
import subprocess, re
from app.controller.logger import Logger


class Status(Cog):
    """상태정보"""

    def __init__(self, bot: Bot):
        self.bot = bot

    @staticmethod
    @Logger.set()
    def get_processor_name():
        if platform.system() == "Windows":
            return platform.processor()
        elif platform.system() == "Darwin":
            os.environ["PATH"] = os.environ["PATH"] + os.pathsep + "/usr/sbin"
            command = "sysctl -n machdep.cpu.brand_string"
            return subprocess.check_output(command, shell=True).strip().decode("utf-8")
        elif platform.system() == "Linux":
            command = "cat /proc/cpuinfo"
            all_info = (
                subprocess.check_output(command, shell=True).strip().decode("utf-8")
            )
            for line in all_info.split("\n"):
                if "model name" in line:
                    return re.sub(".*model name.*:", "", line, 1)
        return ""

    @Logger.set()
    @commands.command(name="status", aliases=["ping", "핑"])
    async def ping(self, ctx):
        await ctx.send("latency: {0} ms".format(round(ctx.bot.latency, 1)))

    @Logger.set()
    @commands.command(name="system", aliases=["sys"])
    async def _system(self, ctx):
        cpu_model = self.get_processor_name()
        cpu_percent = psutil.cpu_percent()
        cpu_count = psutil.cpu_count()
        cpu_freq = psutil.cpu_freq().current / 1024

        mem = psutil.virtual_memory()
        total = round(mem.total / 1024 ** 3)

        avail = mem.available
        available_mem = round(avail / 1024 ** 3, 1)

        source = discord.Embed(
            title="ZERODAY SYSTEM INFORMATION",
            description="```css\nPowered by Disocrd.py\n```",
            color=discord.Color.blurple(),
        )
        source.add_field(
            name="Architecture", value=str(platform.architecture()[0]), inline=False
        )
        source.add_field(name="Machine", value=str(platform.machine()), inline=False)
        source.add_field(name="System", value=str(platform.system()), inline=False)
        source.add_field(
            name="System version", value=str(platform.version()), inline=False
        )
        source.add_field(name="CPU model", value=str(cpu_model), inline=False)
        source.add_field(name="CPU Core", value=str(cpu_count) + " core", inline=False)
        source.add_field(
            name="CPU utilization", value=str(cpu_percent) + " %", inline=False
        )
        source.add_field(
            name="CPU frequency", value=str(cpu_freq) + " GHz", inline=False
        )
        source.add_field(name="RAM capacity", value=str(total) + " GB", inline=False)
        source.add_field(
            name="RAM utilization", value=str(available_mem) + " GB", inline=False
        )
        await ctx.send(embed=source)
