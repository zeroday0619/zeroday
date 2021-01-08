import aiohttp
import discord
import datetime
from discord.ext import commands
from discord.ext.commands import Bot
from discord.ext.commands import Context


class Minecraft(commands.Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.mojang_status_api = "https://status.mojang.com/check"

    @commands.group(name="minecraft", aliases=["mc"])
    async def minecraft(self, ctx: Context):
        """
        mojang status:
            !mc status
        """
        if ctx.invoked_subcommand is None:
            help_cmd = self.bot.get_command("help")
            await ctx.invoke(help_cmd, "minecraft")

    @staticmethod
    async def convert_status(source: str):
        if source.lower() == "green":
            return "**정상**"
        elif source.lower() == "red":
            return "**오류**"
        else:
            return "상태 정보 처리에 오류가 발생하였습니다."

    async def get_mojang_api_status(self, ctx: Context):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.mojang_status_api) as resp:
                if resp.status != 200:
                    return await ctx.send("모장 API 상태정보를 불러오는데 오류가 발생하였습니다.")
                result = await resp.json()
        minecraft_net_server = await self.convert_status(result[0]["minecraft.net"])
        minecraft_session_server = await self.convert_status(result[1]["session.minecraft.net"])
        mojang_account_server = await self.convert_status(result[2]["account.mojang.com"])
        mojang_auth_server = await self.convert_status(result[3]["authserver.mojang.com"])
        mojang_session_server = await self.convert_status(result[4]["sessionserver.mojang.com"])
        mojang_api_server = await self.convert_status(result[5]["api.mojang.com"])
        minecraft_textures_server = await self.convert_status(result[6]["textures.minecraft.net"])
        mojang_com_server = await self.convert_status(result[7]["mojang.com"])

        now = datetime.datetime.now()
        now_time = str(now.strftime('%Y-%m-%d %H:%M:%S'))

        embed=discord.Embed(title="Minecraft Status", url="https://status.mojang.com/check", description="Mojang API 상태정보", color=0x320ee1)
        embed.add_field(name="minecraft.net", value=str(minecraft_net_server), inline=False)
        embed.add_field(name="session.minecraft.net", value=str(minecraft_session_server), inline=False)
        embed.add_field(name="account.mojang.com", value=str(mojang_account_server), inline=False)
        embed.add_field(name="authserver.mojang.com", value=str(mojang_auth_server), inline=False)
        embed.add_field(name="sessionserver.mojang.com", value=str(mojang_session_server), inline=False)
        embed.add_field(name="api.mojang.com", value=str(mojang_api_server), inline=False)
        embed.add_field(name="textures.minecraft.net", value=str(minecraft_textures_server), inline=False)
        embed.add_field(name="mojang.com", value=str(mojang_com_server), inline=False)
        embed.set_footer(text=now_time)
        return await ctx.send(embed=embed)

    @minecraft.command(name="status")
    async def mojang_api_status_check(self, ctx: Context):
        await self.get_mojang_api_status(ctx=ctx)


def setup(bot: Bot):
    bot.add_cog(Minecraft(bot))
