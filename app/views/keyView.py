import discord
import logging
from utils.keyEmbedder import KeyEmbedder

logger = logging.getLogger(__name__)

class KeyView(discord.ui.View, ):
    def __init__(self, list:list, embedder:KeyEmbedder, originalMessageID=None, originalMessageChannel=None):
        super().__init__(timeout=86400)
        self.list = list
        self.embedder = embedder
        self.originalMessageID = originalMessageID
        self.originalMessageChannel = originalMessageChannel

    async def edit_list(self, btn:int, interaction: discord.Interaction):
        await interaction.response.defer()
        for item in self.list:
            if item[0] == interaction.user:
                if item[btn]:
                    item[btn] = False
                else:
                    item[btn] = True
                break
        else:
            self.list.append([interaction.user, btn == 1, btn == 2, btn == 3])
        await interaction.edit_original_response(embed=self.embedder.get_embed(list=self.list), view=self)

    @discord.ui.button(label='DPS', style=discord.ButtonStyle.red, emoji='<:dps:1257129006462144644>')
    async def dps_button(self, interaction: discord.Interaction, button):
        logger.info(f'DPS button pressed by {interaction.user}')
        await self.edit_list(1, interaction)
           
    @discord.ui.button(label='Healer', style=discord.ButtonStyle.green, emoji='<:healer:1257129028276719718>')
    async def healer_button(self, interaction: discord.Interaction, button):
        logger.info(f'Healer button pressed by {interaction.user}')
        await self.edit_list(2, interaction)
        

    @discord.ui.button(label='Tank', style=discord.ButtonStyle.primary, emoji='<:tank:1257129045993459775>')
    async def tank_button(self, interaction: discord.Interaction, button):
        logger.info(f'Tank button pressed by {interaction.user}')
        await self.edit_list(3, interaction)
        

    @discord.ui.button(label='Unsign', style=discord.ButtonStyle.gray)
    async def unsign(self, interaction: discord.Interaction, button):
        logger.info(f'Unsign button pressed by {interaction.user}')
        await interaction.response.defer()
        logger.info(f'Unsign button pressed by {interaction.user}')
        for item in self.list:
            if item[0] == interaction.user:
                self.list.remove(item)
                break
        await interaction.edit_original_response(embed=self.embedder.get_embed(list=self.list), view=self)

    @discord.ui.button(label='Close', style=discord.ButtonStyle.gray)
    async def close(self, interaction: discord.Interaction, button):
        await interaction.response.defer()
        logger.info(f'Close button pressed by {interaction.user}')
        if interaction.user == self.list[0][0]:
            await self.on_timeout()
        else:
            await interaction.followup.send('Only the group leader can close the group', ephemeral=True)

    async def on_timeout(self):
        logger.info('View timed out')
        msg = await self.originalMessageChannel.fetch_message(self.originalMessageID)
        await msg.edit(embed=self.embedder.get_embed(list=self.list, isTimedOut=True), view=None)
    