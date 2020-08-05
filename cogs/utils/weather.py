import discord
import time
import os
from discord.ext import tasks
from discord.ext import commands
from .weather_api import WeatherAPI
from core import bot



class ABCDE:
    def __init__(self):
        self.source = WeatherAPI()

    async def weatherEmergency(self, ctx):
        print(1)
        data = await self.source.load_weather_data()
        d = data['response']['body']['items']['item']
        latest = d
        for a in d:
            print(latest)
            f_read = open('latest.txt', 'r+')
            before = f_read.readline()
            if before != latest:
                bot.get_channel
                await ctx.send(f"{a['other']}\n\n{a['t6']}\n\n{a['t7']}")
                f_write = open('latest.txt', 'w')
                print(latest)
                f_write.write(latest)




class Weather(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.source = ABCDE()

    @commands.command(name='기상특보')
    async def weather(self, ctx):
        while True:
            await self.source.weatherEmergency(ctx=ctx)
            time.sleep(10)