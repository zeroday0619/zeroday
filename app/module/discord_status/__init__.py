import aiohttp
import discord


class DISCORDStatus:
    def __init__(self) -> None:
        self.url = "https://discordstatus.com/api/v2/status.json"

    async def fetch(self) -> dict:
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url) as resp:
                if resp.status != 200:
                    raise Exception(f"Failed to fetch discord status: {resp.status}")
                return await resp.json()
    
    async def create_embed(self) -> discord.Embed:
        data = await self.fetch()
        try:
            embed = discord.Embed(title="DISCORD STATUS", description="discordstatus.com", color=0x00ff00)
            embed.add_field(name="id", value=data["page"]["id"])
            embed.add_field(name="name", value=data["page"]["name"])
            embed.add_field(name="time_zone", value=data["page"]["time_zone"])
            embed.add_field(name="updated_at", value=data["page"]["updated_at"])
            embed.add_field(name="indicator", value=data["status"]["indicator"])
            embed.add_field(name="description", value=data["status"]["description"])
            return embed
        except KeyError:
            raise Exception(f"Failed to create discord status embed: {data}")
