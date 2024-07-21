import discord
from discord import app_commands
from discord.ext import commands
from utils.timestamptool import discordTimestamp
import logging

logger = logging.getLogger(__name__)

class TimestampCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    
    @app_commands.command(description='Outputs a Dynamic Timestamp. It adapts timezones and counts down to the given time!')
    @app_commands.describe(time='HH:MM', day='Day', month='Month', year='Year')
    async def timestamp(self, interaction: discord.Interaction, time: str = None, day: str = None, month: str = None, year: str = None):
        logger.info(f'Timestamp command used by {interaction.user} - {time}')
        try:
            stamp = discordTimestamp(interaction.user, time, day=day, month=month, year=year)
        except ValueError as e:
            await interaction.response.send_message(e, ephemeral=True)
            return
        await interaction.response.send_message(stamp)
        

async def setup(bot):
    await bot.add_cog(TimestampCog(bot))