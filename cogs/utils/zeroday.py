import discord
from discord.ext import commands
from discord.ext.commands import Cog
from discord.ext.commands import Bot


class zeroday(Cog):
    """도움말"""
    def __init__(self, bot: Bot):
        self.bot = bot

    @commands.command(aliases=["초대링크", "봇초대"])
    async def inviteZeroday(self, ctx):
        """초대링크"""
        embedInviteBot = (
            discord.Embed(
                title="ZERODAY BOT 초대 링크 | Ver. 20200612 RC 1347",
                description="초 고음질 음악 재생 기능과 다양한 유틸리티를 탑제한 디스코드 봇 With CTF Tools",
                color=0xabcee9
            )
            .add_field(
                name="ZERODAY BOT Invite Link",
                value="[Invite Link](https://discordapp.com/api/oauth2/authorize?client_id=604882921958146063&permissions=8&redirect_uri=http%3A%2F%2F45.76.216.136%3A5000%2Fcallback&scope=bot)"
            )
        )
        await ctx.send(
            ctx.author.mention,
            embed=embedInviteBot
        )

    @commands.command(pass_context=True)
    async def help(self, context, *module):
        """The help command."""
        content = None

        if not module:
            content = discord.Embed(title='zeroday 사용 가이드',
                                    description='`!help <module>`을 사용하여 zeroday bot 도움말을 보실 수 있습니다.',
                                    colour=discord.Colour.dark_blue())
            module_description = ''
            for x in self.bot.cogs:
                module_description += ('{} - {}'.format(x, self.bot.cogs[x].__doc__) + '\n')
            content.add_field(name='Extension', value=module_description[0:len(module_description) - 1], inline=False)

            await context.send(embed=content)
        else:
            if len(module) > 1:
                content = discord.Embed(title='ERROR', description='Extension ERROR', colour=discord.Colour.red())
                await context.send(embed=content)
            else:
                found = False
                for x in self.bot.cogs:
                    for y in module:
                        if x == y:
                            content = discord.Embed(title=module[0] + ' 명령어 목록', description=self.bot.cogs[module[0]].__doc__)
                            for z in self.bot.get_cog(y).get_commands():
                                if not z.hidden:
                                    content.add_field(name=z.name, value=z.help, inline=False)
                            found = True
                if not found:
                    content = discord.Embed(title='ERROR', description='404 Not Found', colour=discord.Colour.red())
                await context.send(embed=content)