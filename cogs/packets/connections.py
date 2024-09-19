import discord
import asyncio
from discord.ext import commands
from discord import SyncWebhook
from javascript import Once, On
from config import WEBHOOK_URL, OPTIONS


class Connections(commands.Cog):
    def __init__(self, client):
        self.client = client

        @Once(self.client.bot, "spawn")
        def spawn(this):
            embed = discord.Embed(colour=discord.Colour.green(), description="**NerdsFB** Online!")
            webhook = SyncWebhook.from_url(WEBHOOK_URL)
            webhook.send(embed=embed)
            print('[Login] Successful')

        @On(self.client.bot, "end")
        def end(this, event):
            if self.client.reason == "relog":
                return

            embed = discord.Embed(
                colour=discord.Colour.orange(),
                description=f"**Proxy Ended**\nRestarting **{OPTIONS['username']}** in 5 seconds!")
            webhook = SyncWebhook.from_url(WEBHOOK_URL)
            webhook.send(embed=embed)

            async def reconnect():
                await asyncio.sleep(5)
                await self.client.start_mineflayer(restart=True)
            asyncio.run(reconnect())


async def setup(client):
    await client.add_cog(Connections(client))
