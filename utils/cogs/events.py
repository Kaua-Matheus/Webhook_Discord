# SYS
from asyncio import sleep
import os

# Discord
from discord.ext import commands

# .Env
from dotenv import load_dotenv


if load_dotenv():
    WELCOME_CHANNEL = os.getenv("WELCOME_CHANNEL")
else:
    WELCOME_CHANNEL = None


class Event(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

        
    # Events
    ## Welcome
    @commands.Cog.listener(
        name="Welcome new member",
    )
    async def on_member_join(self, member, channel: int | None = WELCOME_CHANNEL):
        if channel == None:
            print("Channel id in .env not found")
            pass
        else:
            welcome_channel = self.client.get_channel(channel) # Insert a channel number
            message = await welcome_channel.send(f"Welcome {member.mention}")

            await sleep(20)

            # Delete the message after the timer
            await message.delete()


async def setup(client: commands.Bot) -> None:
    await client.add_cog(Event(client))