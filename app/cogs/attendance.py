import discord
from discord import app_commands
from discord.ext import commands
import re
import logging

logger = logging.getLogger(__name__)

class AttendanceCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    
    @app_commands.command(description='see which rolemembers are in your voicechannel')
    @app_commands.describe(role='test')
    async def attendance(self, interaction: discord.Interaction, role: str):
        try:
            voice = interaction.user.voice.channel
        except AttributeError:
            await interaction.response.send_message('You are not in a voice channel')
        green = True
        match = re.match(r"<@&(\d+)>", role)
        if match:
            role_id = int(match.group(1))  # Convert the extracted ID to integer
            role_object = interaction.guild.get_role(role_id)  # Get the role object
        else:
            logger.info('Role not found')

        embed = discord.Embed(title='Attendance', description='Shows attendance for chosen role in your current voice channel', color=0x00ff00)
        memberstr = ""
        for member in role_object.members:
            if member.voice != None:
                if member.voice.channel == voice:
                    memberstr += f'✅ {member.display_name}\n'
                else:
                    memberstr += f'❌ {member.display_name}\n'
                    green = False
            else:
                memberstr += f'❌ {member.display_name}\n'
                green = False
            
        embed.add_field(name='Members', value=memberstr, inline=False)
        if not green:
            embed.color = 0xff0000
        await interaction.response.send_message(embed=embed, ephemeral=False)

async def setup(bot):
    await bot.add_cog(AttendanceCog(bot))