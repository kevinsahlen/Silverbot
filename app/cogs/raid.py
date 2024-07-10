import discord
from discord import app_commands
from discord.ext import commands

class RaidCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    
    @app_commands.command(description='Lists all roles of the user')
    async def raid(self, interaction: discord.Interaction):
        voice_state = interaction.author.voice
        if voice_state is not None and voice_state.channel is not None:
            voice_channel_id = voice_state.channel.id
            await interaction.response.send_message(f"The user is currently connected to voice channel with ID: {voice_channel_id}")
        else:
            await interaction.response.send_message("The user is not currently connected to any voice channel.")

async def setup(bot):
    await bot.add_cog(RaidCog(bot))