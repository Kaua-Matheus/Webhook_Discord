# Discord
import discord
from discord.ext import commands
from discord import app_commands, Interaction

# Internal
from ..music.dlp import Downloader

# SYS
from asyncio import run_coroutine_threadsafe
import os


class Music(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.downloader = Downloader()


    # Commands
    @app_commands.command(
        name="join",
        description="Bot entra no canal de voz"
    )
    async def join(self, interaction: Interaction):
        if interaction.user.voice:
            channel = interaction.user.voice.channel
            voice_client = await channel.connect()
            self.downloader.voice_client = voice_client
            await interaction.response.send_message(f"Conectado ao canal: {channel.name}")
        else:
            await interaction.response.send_message("Você precisa estar em um canal de voz!")
        
    
    @app_commands.command(
        name="leave",
        description="Bot sai do canal de voz"
    )
    async def leave(self, interaction: Interaction):
        if self.downloader.voice_client:
            await self.downloader.voice_client.disconnect()
            self.downloader.voice_client = None
            await interaction.response.send_message(f"Desconectado do canal de voz!")
        else:
            await interaction.response.send_message(f"O bot não está conectado em nenhum canal!") # Insert self.name in bot


    @app_commands.command(
        name="play",
        description="Toca uma música"
    )
    @app_commands.describe(query="Nome ou URL da música")
    async def play(self, interaction: Interaction, query: str):
        if not self.downloader.voice_client: # Add to connect in the channel if it exists without need to /join
            await interaction.response.send_message(f"Use /join primeiro para me conectar a um canal!")
            return

        await interaction.response.defer()

        file_path = self.downloader.download(query)

        if not file_path:
            await interaction.followup.send("Erro ao baixar música")
            return
        
        # If is already playing, add to queue
        if self.downloader.voice_client.is_playing():
            self.downloader.add_to_queue(file_path)
            await interaction.followup.send(f"Música adicionada a fila: {query}")
        else:
            await self._play_song(interaction, file_path, query)

    
    @app_commands.command(
        name="stop",
        description="Para a música atual"
    )
    async def stop(self, interaction: Interaction):
        if self.downloader.voice_client and self.downloader.voice_client.is_playing():
            self.downloader.voice_client.stop()
            self.downloader.queue.clear() # Add a way to go back playing
            await interaction.response.send_message("Música parada!")
        else:
            await interaction.response.send_message("Não há música tocando!")


    # @app_commands.command(
    #     name="continue",
    #     description="Retorna a música de onde parou"
    # )
    # async def stop(self, interaction: Interaction):
    #     if self.downloader.voice_client and not self.downloader.voice_client.is_playing():
    #         self.downloader.voice_client.play()
    #         await interaction.response.send_message("Continuando música..")
    #     else:
    #         await interaction.response.send_message("Não há música tocando!")


    @app_commands.command(
        name="queue",
        description="Mostra a fila de músicas"
    )
    async def stop(self, interaction: Interaction):
        if not self.downloader.queue:
            await interaction.response.send_message("A fila está vazia!")
            return
        else:
            queue_list = "\n".join([
                f"{i+1}. {os.path.basename(song).replace(".mp3, ")}"
                for i, song in enumerate(self.downloader.queue[:10]) # Only the 10 first
            ])

            embed = discord.Embed(
                title="Fila de Músicas",
                description=queue_list,
                color=0x0099ff
            )

            if self.downloader.current:
                embed.add_field(
                    name="Tocando agora:",
                    value=self.downloader.current,
                    inline=False
                )

            await interaction.response.send_message(embed=embed)


    # Privated
    async def _play_song(self, interaction, file_path, query):
        try:
            source = discord.FFmpegPCMAudio(file_path)
            self.downloader.voice_client.play(
                source,
                after=lambda e: run_coroutine_threadsafe(
                    self._song_finished(interaction),
                    self.client.loop
                )
            )
            self.downloader.current = query

            embed = discord.Embed(
                title="Tocando agora",
                description=f"**{query}**",
                color=0x00ff00
            )

            if hasattr(interaction, "followup"):
                await interaction.followup.send(embed=embed)
            else:
                await interaction.response.send_message(embed=embed)

        except Exception as err:
            await interaction.followup.send(f"Erro ao tocar a música: {err}")

    
    async def _song_finished(self, interaction):
        next_song = self.downloader.next_music()
        if next_song:
            file_name = os.path.basename(next_song).replace(".mp3", "")
            await self._play_song(interaction, next_song, file_name)


async def setup(client: commands.Bot) -> None:
    await client.add_cog(Music(client))