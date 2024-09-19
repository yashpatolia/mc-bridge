import discord
import asyncio
from discord.ext import commands
from discord import app_commands
from config import OPTIONS
from javascript import require

mineflayer = require('mineflayer')


class Relog(commands.Cog):
    def __init__(self, client):
        self.client = client

    @app_commands.command(name="relog", description="Relogs the bridge bot")
    async def relog(self, interaction: discord.Interaction):
        await interaction.response.defer()

        embed = discord.Embed(
            colour=discord.Colour.orange(),
            description=f"Relogging **{OPTIONS['username']}** in 5 seconds!")
        await interaction.edit_original_response(embed=embed)

        print(f"Relogging {OPTIONS['username']} in 5 seconds!")
        self.client.reason = "relog"
        self.client.bot.end()
        await asyncio.sleep(5)
        await self.client.start_mineflayer(restart=True)

async def setup(client):
    await client.add_cog(Relog(client))
