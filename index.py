import os
import logging

import discord
from discord.ext import commands
from discord_slash import SlashCommand

from config import CONSTANTS

file_log = logging.FileHandler('lonir.log', encoding='utf-8')
console_out = logging.StreamHandler()
logging_level = logging.DEBUG if CONSTANTS.DEBUG else logging.INFO

logging.basicConfig(
    handlers=(file_log, console_out),
    format='[%(asctime)s] %(module)s --> %(levelname)s: %(message)s',
    level=logging_level
)
log = logging.getLogger('logger')
log.info('Logs connected!')

intents = discord.Intents.all()

lonir = commands.Bot(token=CONSTANTS.TOKEN, command_prefix='/', intents=intents)
lonir.remove_command('help')
slash = SlashCommand(lonir, sync_commands=True, sync_on_cog_reload=True)

log.info('Cogs loading...')
for cog_name in os.listdir('./cogs'):
    if cog_name.endswith('.py'):
        lonir.load_extension(f'cogs.{cog_name[:-3]}')
        log.info(f'----Cog {cog_name} loaded')
log.info('Cogs loaded!')

lonir.run(CONSTANTS.TOKEN)