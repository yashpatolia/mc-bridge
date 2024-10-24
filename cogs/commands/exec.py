import discord
from discord.ext import commands
from discord import app_commands
from config import OWNER_ID, EXEC_PERMS


class Exec(commands.Cog):
    def __init__(self, client):
        self.client = client

    @app_commands.command(name="exec", description="Execute a command")
    @app_commands.describe(command="Command to run")
    async def exec(self, interaction: discord.Interaction, command: str):
        await interaction.response.defer()
        if interaction.user.id not in EXEC_PERMS or interaction.user.id != OWNER_ID:
            embed = discord.Embed(colour=discord.Colour.red(), description="Not sufficient permissions!")
            await interaction.edit_original_response(embed=embed)
            return

        self.client.bot.chat(f"/{command}")
        await self.client.log(interaction, command)
        embed = discord.Embed(colour=discord.Colour.green(), description=f"**Command Executed:** /{command}")
        await interaction.edit_original_response(embed=embed)


async def setup(client):
    await client.add_cog(Exec(client))
