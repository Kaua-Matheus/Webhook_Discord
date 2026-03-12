# Discord
import discord
from discord.ext import commands
from discord import app_commands, Interaction

# Internal
from ..music.dlp import Downloader

# SYS
from asyncio import run_coroutine_threadsafe


class Music(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.downloader = Downloader()
        self.queue = []
        self.current_song = None
        self.voice_client = None
        self.is_paused = False


    # Commands
    ## Join
    @app_commands.command(
        name="join",
        description="Bot entra no canal de voz"
    )
    async def join(self, interaction: Interaction):
        if interaction.user.voice:
            channel = interaction.user.voice.channel
            self.voice_client = await channel.connect()
            await interaction.response.send_message(f"Conectado ao canal: {channel.name}")
        else:
            await interaction.response.send_message("Você precisa estar em um canal de voz!")
        
    
    ## Leave
    @app_commands.command(
        name="leave",
        description="Bot sai do canal de voz"
    )
    async def leave(self, interaction: Interaction):
        if self.voice_client:
            await self.voice_client.disconnect()
            self.voice_client = None
            self.queue.clear()
            self.current_song = None
            await interaction.response.send_message(f"Desconectado do canal de voz!")
        else:
            await interaction.response.send_message(f"O bot não está conectado em nenhum canal!") # Insert self.name in bot


    ## Play
    @app_commands.command(
        name="play",
        description="Toca uma música"
    )
    @app_commands.describe(query="Nome ou URL da música")
    async def play(self, interaction: Interaction, query: str):
        if not self.voice_client:
            await interaction.response.send_message(f"Use /join primeiro para me conectar a um canal!")
            return

        await interaction.response.defer()

        file_path = self.downloader.download(query)

        if not file_path:
            await interaction.followup.send("Erro ao baixar música")
            return
        
        # If is already playing, add to queue
        if self.voice_client.is_playing():
            self.queue.append({"path": file_path, "title": query})
            await interaction.followup.send(f"Música adicionada a fila: {query}")
        else:
            await self._play_song(interaction, file_path, query)

    
    ## Stop
    @app_commands.command(
        name="stop",
        description="Para a música e limpa a fila"
    )
    async def stop(self, interaction: Interaction):
        if self.voice_client and (self.voice_client.is_playing() or self.voice_client.is_paused()):
            self.voice_client.stop()
            self.queue.clear()
            self.current_song = None
            self.is_paused = False
            await interaction.response.send_message("Música parada!")

            embed = discord.Embed(
                title="Reprodução Parada",
                description="Música parada e fila limpa",
                color=0xff0000
            )
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("Não há música tocando!")


    ## Pause
    @app_commands.command(
        name="pause",
        description="Para a música atual"
    )
    async def pause(self, interaction: Interaction):
        if self.voice_client and self.voice_client.is_playing():
            self.voice_client.pause()
            self.is_paused = True

            embed = discord.Embed(
                title="Música pausada",
                description=f"**{self.current_song['title'] if self.current_song else 'Música atual'}**",
                color=0xffaa00
            )
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("Não há música tocando para pausar!")

    
    ## Resume
    @app_commands.command(
        name="resume",
        description="Retoma a música pausada"
    )
    async def resume(self, interaction: Interaction):
        if self.voice_client and not self.voice_client.is_playing():
            self.voice_client.resume()
            self.is_paused = False

            embed = discord.Embed(
                title="Música Retomada",
                description=f"**{self.current_song['title'] if self.current_song else "Música atual"}**",
                color=0x00ff00
            )
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("Não há música pausada para retomar!")


    ## Skip
    @app_commands.command(
        name="skip",
        description="Pula para a próxima música"
    )
    async def skip(self, interaction: Interaction):
        if self.voice_client and (self.voice_client.is_playing() or self.voice_client.is_paused()):
            if self.queue:
                self.voice_client.stop()

                embed = discord.Embed(
                    title="Música Pulada",
                    description=f"Pulando: **{self.current_song['title'] if self.current_song else 'Música atual'}**",
                    color=0x0099ff
                )
                await interaction.response.send_message(embed=embed)
            else:
                self.voice_client.stop()
                self.current_song = None
                self.is_paused = False

                embed = discord.Embed(
                        title="Música Parada",
                        description=f"Não há mais músicas na fila",
                        color=0xff0000
                    )
                await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("Não há música tocando para pular!")


    ## Queue
    @app_commands.command(
        name="queue",
        description="Mostra a fila de músicas"
    )
    async def show_queue(self, interaction: Interaction):
        embed = discord.Embed(
            title="Fila de músicas",
            description=f"**{self.current_song["title"]}**"
        )

        if self.queue:
            queue_list = "\n".join([
                f"`{i+1}. ` **{song_name["title"]}**" 
                for i, song_name in enumerate(self.queue[:10])  # Only 10
            ])

            embed.add_field(
                name=f"Próximas ({len(self.queue)} música{'s' if len(self.queue) != 1 else ''}):",
                value=queue_list
            )
        else:

            if not self.current_song:
                embed.description("A fila está vazia!")
            else:
                embed.add_field(
                    name="Próximas:",
                    value="Nenhuma música na fila"
                )

        await interaction.response.send_message(embed=embed)


    ## Now Playing
    @app_commands.command(
        name="nowplaying",
        description="Mostra a música tocando atualmente"
    )
    async def now_playing(self, interaction: Interaction):
        if self.current_song:
            status = "Pausada" if self.is_paused else "Tocando"

            embed = discord.Embed(
                title=f"{status} Agora",
                description=f"**{self.current_song['title']}**",
                color=0x00ff00 if not self.is_paused else 0xffaa00
            )

            embed.add_field(
                name="Fila:",
                value=f"{len(self.queue)} música{'s' if len(self.queue) != 1 else ''} aguardando",
            )

            await interaction.response.send_message(embed=embed)

        else:
            await interaction.response.send_message("Nenhuma música tocando no momento")


    # Privated
    ## Play Song
    async def _play_song(self, interaction, file_path, title):
        try:
            source = discord.FFmpegPCMAudio(file_path)
            self.voice_client.play(
                source,
                after=lambda e: run_coroutine_threadsafe(
                    self._song_finished(interaction),
                    self.client.loop
                )
            )

            self.current_song = {"path": file_path, "title": title}
            self.is_paused = False

            embed = discord.Embed(
                title="Tocando agora",
                description=f"**{title}**",
                color=0x00ff00
            )

            if hasattr(interaction, "followup"):
                await interaction.followup.send(embed=embed)
            else:
                await interaction.response.send_message(embed=embed)

        except Exception as err:
            await interaction.followup.send(f"Erro ao tocar a música: {err}")


    ## Song Finished
    async def _song_finished(self, interaction):
        if self.queue:
            next_song = self.queue.pop(0)
            await self._play_song(interaction, next_song["path"], next_song["title"])
        else:
            self.current_song = None


async def setup(client: commands.Bot) -> None:
    await client.add_cog(Music(client))