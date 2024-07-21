import discord
from discord import app_commands
from discord.ext import commands
import logging

logger = logging.getLogger(__name__)

class FixTimeZoneCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(description='Tell me your country code and your timezone will be accounted for in other commands!')
    async def fixtimezone(self, interaction: discord.Interaction):
#START OF FUNCTION-------------------------------------------------------------------------------------------
        await interaction.response.send_message(f'[Click to set your timezone!](http://37.27.94.42:3000/?userid={interaction.user.id}&username={interaction.user.name})', ephemeral=True)
#END OF FUNCTION---------------------------------------------------------------------------------------------

async def setup(bot):
    await bot.add_cog(FixTimeZoneCog(bot))