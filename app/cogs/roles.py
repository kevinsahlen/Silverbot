import discord
from discord import app_commands
from discord.ext import commands

class RolesCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(description='Lists all roles of the user')
    async def roles(self, interaction: discord.Interaction):
#START OF FUNCTION--------------------------------------------------------------------------------
        roles = [role.name for role in interaction.user.roles if role.name != "@everyone"]
        roles_message = ', '.join(roles) if roles else 'You have no roles.'
        await interaction.response.send_message(f'Your roles are: {roles_message}')
#END OF FUNCTION----------------------------------------------------------------------------------

async def setup(bot):
    await bot.add_cog(RolesCog(bot))