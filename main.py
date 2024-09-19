import discord
import os
import asyncio
import time
from discord.ext import commands
from discord import SyncWebhook
from config import TOKEN, LOGS_WEBHOOK_URL, OPTIONS
from javascript import require

mineflayer = require('mineflayer')


class Client(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=discord.Intents().all())
        self.online = True
        self.blocked = False
        self.bot = None
        self.fragbot_queue = []
        self.reason = None

        self.save_guild_list = False
        self.guild_list = []
        self.save_motd_preview = False
        self.guild_motd_preview = []
        self.guild_invite = ""

    async def start_mineflayer(self, restart: bool = False):
        self.bot = mineflayer.createBot(OPTIONS)

        if restart:
            await self.reload_extension("cogs.packets.connections")
            await self.reload_extension("cogs.bridge.bridge")
            await self.reload_extension("cogs.packets.message_handler")
            self.reason = None

    async def log(self, interaction, command):
        try:
            original_message = await interaction.original_response()
            embed = discord.Embed(colour=discord.Colour.teal(),
                                description=f"**User:** {interaction.user.name}\n"
                                            f"**Command:** /{command}\n"
                                            f"**Jump to Message:** {original_message.jump_url}\n"
                                            f"**Timestamp:** <t:{str(time.time()).split('.')[0]}>")
            webhook = SyncWebhook.from_url(LOGS_WEBHOOK_URL)
            webhook.send(embed=embed, username="Command Logging", avatar_url=interaction.user.display_avatar.url)
        except Exception as e:
            pass

    async def setup_hook(self):
        await self.start_mineflayer()
        for folder in os.listdir("./cogs"):
            for file in os.listdir(f"./cogs/{folder}"):
                if file.endswith(".py"):
                    await self.load_extension(f"cogs.{folder}.{file[:-3]}")

    async def on_ready(self):
        print(f"Logged in as {self.user.name} (ID: {self.user.id})!")
        game = discord.Game(name="Guild Bridge & Frag Bot")
        await self.change_presence(activity=game, status=discord.Status.online)
        synced = await self.tree.sync()
        print(f"Synced {len(synced)} slash commands!")


async def run_bot():
    async with Client() as client:
        await client.start(TOKEN)

asyncio.run(run_bot())
