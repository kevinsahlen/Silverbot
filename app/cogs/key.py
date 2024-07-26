import discord
from discord import app_commands
from discord.ext import commands
from views.keyView import KeyView
from utils.keyEmbedder import KeyEmbedder
from utils.timestamptool import discordTimestampKey
import logging
import re

logger = logging.getLogger(__name__)

class KeyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(description='Start forming a key group. Use @mention to add friends to the group!')
    @app_commands.describe(
        premades='@mention friends to add them to list!',
        description='Description of the group',
        starttime='Time the group starts in HH:MM')
    async def key(
        self,
        interaction: discord.Interaction,
        premades: str = None,
        description: str = '',
        starttime: str = None): 

#START OF FUNCTION-------------------------------------------------------------------------------------------
        logger.info(f'Key command used by {interaction.user} - {premades} - {description} - {starttime}')
        if starttime != None:
            try:
                starttime = discordTimestampKey(input_HHMM=starttime, user=interaction.user, input_day=None, input_month=None, input_year=None)
            except ValueError as e:
                await interaction.response.send_message(e, ephemeral=True)
                return
        #final list that gets added to embed
        embed_list = []
        #Always add command user to list
        embed_list.append([interaction.user, False, False, False])
        #Add all premades that are not None to embed_list
        if premades != None:
            iterate_premade = premades.split()
            for i in iterate_premade:
                if i != None:
                    if re.match(r"^<@\d{18}>$", i):#regex pattern for discord user mention
                        user = await self.bot.fetch_user(int(i[2:-1]))
                        if [user, False, False, False] not in embed_list:
                            embed_list.append([user, False, False, False])
                            logger.info(f'Added {i} to list')

                        else:#[user, False, False, False] not in embed_list
                            logger.info(f'{i} is already in list, skipping')
                    else:#re.match(pattern, i):
                        logger.info(f'{i} is not a valid user mention, skipping')
                else:#i != None:
                    logger.info(f'{i} is None, skipping')
        embedder = KeyEmbedder(
            list=embed_list,
            description_input=description,
            start_time=starttime)
        view = KeyView(
            list=embed_list,
            embedder=embedder)
        #create group forming message
        await interaction.response.send_message(
            embed=embedder.get_embed(),
            view=view,
            ephemeral=False)
        #save channel and message id to keyView object, only used for closing the view after timeout
        originalMessage = await interaction.original_response()
        view.originalMessageID = originalMessage.id
        view.originalMessageChannel = originalMessage.channel
#END OF FUNCTION-------------------------------------------------------------------------------------------

async def setup(bot):
    await bot.add_cog(KeyCog(bot))