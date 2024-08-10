import discord
import logging

logger = logging.getLogger(__name__)

class TestModal(discord.ui.Modal):
    def __init__(self) -> None:
        super().__init__(title='Test Modal')
        self.add_item(discord.ui.TextInput(label='Short Input'))
        self.add_item(discord.ui.TextInput(label='Long Input', style=discord.TextStyle.long))

    async def on_submit(self, interaction: discord.Interaction) -> None:
        await interaction.response.send_message(self.children[0].value, ephemeral=True)