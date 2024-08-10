from discord import app_commands, Interaction
from discord.ext import commands
import logging
import dotenv

logger = logging.getLogger(__name__)
dotenv.load_dotenv()
link = dotenv.dotenv_values()['TZ_LINK']
#LOCAL
#TZ_LINK = 'localhost'
#TZ_LINK_REAL = '[serverip]'

#SERVER
#TZ_LINK = '[serverip]'
#TZ_LINK_DUMMY = 'localhost'

class FixTimeZoneCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(description='Saves your timezone for correct command functionality')
    async def fixtimezone(self, interaction: Interaction):
#START OF FUNCTION-------------------------------------------------------------------------------------------
        await interaction.response.send_message(f'[Click to set your timezone!](http://{link}:3000/fixtimezone/readuser?userid={interaction.user.id}&username={interaction.user.name})', ephemeral=True)

#END OF FUNCTION---------------------------------------------------------------------------------------------
async def setup(bot):
    await bot.add_cog(FixTimeZoneCog(bot))