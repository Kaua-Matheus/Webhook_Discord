# SYS
from asyncio import sleep

# Discord
from discord.ext import commands
from discord import app_commands, Interaction
from discord import Embed

class Command(commands.Cog):
    def __init__(self, client:commands.Bot):
        self.client = client


    # Commands
    ## Debug
    @app_commands.command(
        name="debug",
        description="Check if the bot is working",
    )
    async def debug(self, interaction: Interaction):
        await interaction.response.send_message(f"Hello {interaction.user.mention}!")
    
    ## Ping
    @app_commands.command(
        name="ping",
        description="Check the bot latency",
    )
    async def ping(self, interaction: Interaction):
        await interaction.response.send_message(f"Pong! {round(self.client.latency * 1000)}ms")

    ## Server Information
    @app_commands.command(
        name="info",
        description="Show the info of the server",
    )
    async def info(self, interaction: Interaction):
        guild = interaction.guild
        await interaction.response.send_message(
            f"**Server**: {guild.name}\n"
            f"**Members**: {guild.member_count}\n"
            f"**ID**: {guild.id}"
        )

    ## Embed
    @app_commands.command(
        name="embed",
        description="embed card",
    )
    async def embed(self, interaction: Interaction):
        embed = Embed(
            title="Título",
            description="Embed Description",
            colour=11598249,
        )

        embed.set_author(
            name=interaction.user.name, 
            icon_url="" # Author Icon URL
        )

        embed.set_thumbnail(
            url="" # Thumbnail Icon / Gif URL
        )

        embed.set_image(
            url="" # Image URL
        )

        await interaction.response.send_message(embed=embed)

    ## Plus
    @app_commands.command(
        name="plus",
        description="Make a plus between two numbers"
    )
    @app_commands.describe(
         num_1="First Number",
         num_2="Second Number"
    )
    async def plus(self, interaction: Interaction, num_1: int, num_2: int):
            result = num_1 + num_2
            await interaction.response.send_message(f"The result is {result}")

    # Events
    @commands.Cog.listener(
        name="Welcome new member",
    )
    async def on_member_join(self, member, channel: int):
        welcome_channel = self.client.get_channel(channel) # Insert a channel number
        message = await welcome_channel.send(f"Welcome {member.mention}")

        await sleep(20)

        # Delete the message after the timer
        await message.delete()



async def setup(client: commands.Bot) -> None:
    await client.add_cog(Command(client))