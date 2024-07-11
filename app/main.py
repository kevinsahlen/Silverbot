#IMPORTS------------------------------------------------
import discord
from discord.ext import commands
import asyncio
import os
from dotenv import load_dotenv
import logging
import datetime

#INITIALIZE---------------------------------------------
load_dotenv()
logger = logging.getLogger(__name__)
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=os.getenv('PREFIX'), intents=intents)

#LOADING COGS-------------------------------------------
async def main():
    logging.basicConfig(level=logging.INFO)
    logger.info('Starting bot')
    cogs_folder = 'cogs'
    for filename in os.listdir(os.path.join(os.path.dirname(__file__), cogs_folder)):
        if filename.endswith('.py'):
            cog_name = filename[:-3]
            cog_path = f'{cogs_folder}.{cog_name}'
            logger.info(f'Loading cog {cog_name}')
            await bot.load_extension(cog_path)
    await bot.start(os.getenv('TOKEN_TEST')) #'TOKEN' = Silverbot, 'TOKEN_TEST' = SilverDummy(test bot)

#OWNER COMMANDS------------------------------------------
#_syncslash - syncs all global commands
#_loadedcogs - checks loaded cogs
#_loginput - logs whatever input is given

@commands.command(description='Sync all global commands')
@commands.is_owner()
async def syncslash(ctx: commands.Context):
    logger.info('Syncing global commands')
    await bot.tree.sync()
bot.add_command(syncslash)

@commands.command(description='check loaded cogs')
@commands.is_owner()
async def loadedcogs(ctx: commands.Context):
    logger.info('Checking loaded cogs')
    for cog in bot.cogs:
        logger.info(f'Loaded cog: {cog}')
bot.add_command(loadedcogs)

@commands.command(description='log input')
@commands.is_owner()
async def loginput(ctx: commands.Context, input: str):
    logger.info(f'Log input command: {input}')
bot.add_command(loginput)

#BOT EVENTS--------------------------------------------
@bot.event
async def on_ready():
    logger.info(f'Logged in as {bot.user}')

@bot.event
async def on_resumed():
    logger.info(f'Bot resumed {datetime.datetime.now()}')

@bot.event
async def on_disconnect():
    logger.info('Bot disconnected')

@bot.event
async def on_command_error(ctx, error):
    logger.error(f'Error in command: {error}')

#RUN MAIN----------------------------------------------
if __name__ == "__main__":
    asyncio.run(main())