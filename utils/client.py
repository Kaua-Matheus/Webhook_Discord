# Discord.py
import discord
from discord.ext import commands

class Bot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()
        super().__init__(
            command_prefix="$",
            intents=intents,
        )

    async def setup_hook(self):
        await self.load_extension("utils.cogs.commands")
        await self.load_extension("utils.cogs.events")
        print("Loading bot...")
        
        await self.tree.sync()

    async def on_ready(self):
        print(f"Bot {self.user} wake up successfully..")
