# Build-in Packages
import os

# Discord.py
import discord

# .Env
from dotenv import load_dotenv

# Client
from utils.client import Bot

if load_dotenv():
    print(".env file loaded successfully")

    try:

        # Bot Token Definition
        TOKEN: str = os.getenv("TOKEN")

        # Bot instance
        bot = Bot()

        # First Command of Capital
        @bot.tree.command(name="hello-world", description="First Command")
        async def helloworld(interaction:discord.Interaction):
            await interaction.response.send_message(f"Hello {interaction.user.mention}!")

        bot.run(TOKEN)
        
    
    except Exception as err:
        print(f"Generic error: {err}")
else:
    print("Couldn't load .env file")