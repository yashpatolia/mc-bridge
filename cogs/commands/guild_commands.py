import asyncio
import discord
from discord.ext import commands
from discord import app_commands
from config import STAFF_ROLE, OWNER_ID


class GuildCommands(commands.GroupCog, name="guild"):
    def __init__(self, client):
        self.client = client
        super().__init__()

    @app_commands.command(name="list", description="Lists guild members!")
    async def list(self, interaction):
        await interaction.response.defer()
        self.client.bot.chat("/g list")
        await asyncio.sleep(0.75)

        guild_string = "".join(f"{i.lstrip()}\n" for i in self.client.guild_list)
        embed = discord.Embed(colour=discord.Colour.teal(),
                              description=f"```{guild_string}```")
        self.client.guild_list.clear()
        await interaction.edit_original_response(embed=embed)
        await self.client.log(interaction, "g list")

    @app_commands.command(name="online", description="Lists guild members!")
    async def online(self, interaction):
        await interaction.response.defer()
        self.client.bot.chat("/g online")
        await asyncio.sleep(0.75)

        guild_string = "".join(f"{i.lstrip()}\n" for i in self.client.guild_list)
        embed = discord.Embed(colour=discord.Colour.teal(),
                              description=f"```{guild_string}```")
        self.client.guild_list.clear()
        await interaction.edit_original_response(embed=embed)
        await self.client.log(interaction, "g online")

    # @app_commands.command(name="motd-preview", description="Preview guild MOTD!")
    # async def motd_preview(self, interaction):
    #     await interaction.response.defer()
    #     self.client.bot.chat("/g motd preview")
    #     await asyncio.sleep(0.75)

    #     motd_preview_string = "".join(f"{i.lstrip()}\n" for i in self.client.guild_motd_preview)
    #     embed = discord.Embed(colour=discord.Colour.orange(),
    #                           description=f"```{motd_preview_string}```")
    #     self.client.guild_motd_preview.clear()
    #     await interaction.edit_original_response(embed=embed)
    #     await self.client.log(interaction, "g motd preview")

    @app_commands.command(name="invite", description="Invite member!")
    @app_commands.describe(ign="IGN")
    async def invite(self, interaction, ign: str):
        await interaction.response.defer()
        role = discord.utils.get(interaction.guild.roles, id=STAFF_ROLE)
        if role in interaction.user.roles or interaction.user.id == OWNER_ID:
            self.client.bot.chat(f"/g invite {ign}")
            await asyncio.sleep(0.75)
            embed = discord.Embed(colour=discord.Colour.green(),
                                  description=f"{self.client.guild_invite}")
            self.client.guild_invite = ""
            await self.client.log(interaction, f"g invite {ign}")
        else:
            embed = discord.Embed(colour=discord.Colour.red(), description="You do not have sufficient permissions!")
        await interaction.edit_original_response(embed=embed)


async def setup(client):
    await client.add_cog(GuildCommands(client))
