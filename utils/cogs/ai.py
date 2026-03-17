# Discord
import discord
from discord.ext import commands
from discord import app_commands, Interaction

# Internal
from ..openai.chat import Llama


class AI(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.llama = Llama()


    # Commands
    ## Send Message
    @app_commands.command(
        name="ai_completion",
        description="Use the Llama-3.1-8b-instant to answer a question",
    )
    @app_commands.describe(question="Pergunta a ser feita para o Llama-3.1")
    async def ai_completion(self, interaction: Interaction, question: str):
        if question == "":
            embed = discord.Embed(
                title="Erro",
                description=f"**Erro: Por favor, insira uma pergunta válida.**",
                color=0xff0000
            )

            await interaction.response.send_message(f"")
            return
        else:
            answer = self.llama.send_message(question)

            embed = discord.Embed(
                title="Resposta IA",
                description=f"**{answer}**", # 4096 Char Limit
                color=0x00ff00
            )
            await interaction.response.send_message(embed=embed)
            return


async def setup(client: commands.Bot) -> None:
    await client.add_cog(AI(client))