import logging, re

import discord
from discord.ext import commands
from discord_slash.context import SlashContext
from discord_slash.model import SlashMessage

from config import CONSTANTS, database

log = logging.getLogger('logger')

class Events(commands.Cog):
    def __init__(self, lonir):
        self.lonir = lonir

    @commands.Cog.listener()
    async def on_connect(self):
        log.info('Connecting...')
    
    @commands.Cog.listener()
    async def on_ready(self):
        log.info('Connected!')

        database.database.prepare()

        log.info('!!! READY !!!')
    
    @commands.Cog.listener()
    async def on_message(self, msg: SlashMessage):
        if msg.content != '':
            log.info(f'{msg.guild.name} {msg.channel.name} {msg.author.name}: {msg.content}')
        
        if msg.author.bot:
            return
        
        economy = database.database(f'''SELECT economy
        FROM guilds
        WHERE id = {msg.guild.id}''', 'one')[0]
        if economy:
            scores = database.database(f'''SELECT scores
            FROM users
            WHERE guild_id = {msg.guild.id} AND id = {msg.author.id}''', 'one')[0]
            level = CONSTANTS.SCORES_TO_LEVEL(scores)
            if msg.content[0] != self.lonir.command_prefix and not re.match(CONSTANTS.EMOJI_FILTER, msg.content) and level < CONSTANTS.MAX_LEVEL:
                got_scores = CONSTANTS.SCORES_FROM_LEN(len(msg.content))
                scores += got_scores
                database.database(f'''UPDATE users
                SET scores = {scores}
                WHERE guild_id = {msg.guild.id} AND id = {msg.author.id}''')
                log.info(f'{msg.author} from {msg.guild.name} got {got_scores} scores')
                
                next_level = CONSTANTS.SCORES_TO_LEVEL(scores)
                if level < next_level:
                    embed = discord.Embed(
                        title=f'Повышение уровня {msg.author.name}!',
                        description=f'{msg.author.name}, поздравляю с повышением уровня до {next_level}! :tada:',
                        colour=discord.Colour.from_rgb(*CONSTANTS.CLR)
                    )
                    await msg.reply(embed=embed)


    @commands.Cog.listener()
    async def on_member_join(member: discord.Member):
        log.info(f'To {member.guild.name} joined {member.name}')

        database.database(f'''INSERT INTO users (guild_id, id)
        VALUES ({member.guild.id}, {member.id})''')

    @commands.Cog.listener()
    async def on_member_remove(member: discord.Member):
        log.info(f'From {member.guild.name} removed {member.name}')

        database.database(f'''DELETE FROM users
        WHERE guild_id = {member.guild.id} AND id = {member.id}''')
    
    @commands.Cog.listener()
    async def on_guild_join(guild: discord.Guild):
        log.info(f'Lonir has added to {guild.name} ({guild.id})')

        database.database(f'''INSERT INTO guilds (id)
        VALUES ({guild.id})''')
    
    @commands.Cog.listener()
    async def on_guild_remove(guild: discord.Guild):
        log.info(f'Lonir has removed from {guild.name} ({guild.id})')

        database.database(f'''DELETE FROM guilds
        WHERE id = {guild.id};
        
        DELETE FROM users
        WHERE guild_id = {guild.id};''')

    @commands.Cog.listener()
    async def on_command(self, ctx: SlashContext):
        log.info(f'{ctx.guild.name} {ctx.author.name} called {ctx.command.name}({ctx.args[2:]}) execution...')

def setup(lonir):
    lonir.add_cog(Events(lonir))