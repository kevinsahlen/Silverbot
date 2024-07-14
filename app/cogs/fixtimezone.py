import discord
from discord import app_commands
from discord.ext import commands
import logging
from utils.db import Database

logger = logging.getLogger(__name__)

class FixTimeZoneCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    
    @app_commands.command(description='Tell me your country code and your timezone will be accounted for in other commands!')
    @app_commands.describe(country_code='Country code for the user, 2 letters. if unsure, google "[your country] alpha-2"')
    async def fixtimezone(self, interaction: discord.Interaction, country_code: str):
        logger.info(f'Key command used by {interaction.user} - {country_code}')
        if country_code is None:
            await interaction.response.send_message('Please provide a country code', ephemeral=True)
            return
        if len(country_code) != 2:
            await interaction.response.send_message('Country code must be 2 letters', ephemeral=True)
            return
        await interaction.response.send_message(f'Country code set to {country_code}', ephemeral=True)
        #Database.setCountryCode(interaction.user, countryCode)
        Database.setCountryCode(interaction.user, country_code)
        logger.info(f'Country code set to {country_code} for {interaction.user}')
        
async def setup(bot):
    await bot.add_cog(FixTimeZoneCog(bot))