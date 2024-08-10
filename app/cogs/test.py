from discord import app_commands, Interaction
from discord.ext import commands
from dotenv import load_dotenv, dotenv_values
from utils.testModal import TestModal

load_dotenv()

class TestCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(description='Test command')
    async def test(self, interaction: Interaction):
        if interaction.user.id != int(dotenv_values()['AUTHOR']):
            await interaction.response.send_message('You are not the author of this bot!')
            return
        modal = TestModal()
        await interaction.response.send_modal(modal)
async def setup(bot):
    await bot.add_cog(TestCog(bot))