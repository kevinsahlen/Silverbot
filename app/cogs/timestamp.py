import discord
from discord import app_commands
from discord.ext import commands
from utils.timestamptool import TimestampTool
import logging

logger = logging.getLogger(__name__)

class TimestampCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    
    @app_commands.command(description='Outputs a Dynamic Timestamp. It adapts timezones and counts down to the given time!')
    @app_commands.describe(time='HH:MM')
    async def timestamp(self, interaction: discord.Interaction, time: str = None):
        logger.info(f'Timestamp command used by {interaction.user} - {time}')
        await interaction.response.send_message(TimestampTool.discordTimestamp(time))

async def setup(bot):
    await bot.add_cog(TimestampCog(bot))