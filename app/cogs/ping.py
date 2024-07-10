import discord
from discord import app_commands
from discord.ext import commands

class PingCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    
    @app_commands.command(description='Pings the bot')
    async def ping(self, interaction: discord.Interaction):
        
        await interaction.response.send_message('I\'m Awake!')

async def setup(bot):
    await bot.add_cog(PingCog(bot))