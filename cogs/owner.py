import logging

import discord
from discord.ext import commands
import psycopg2

from config import database

log = logging.getLogger('logger')

class Owner(commands.Cog):
    def __init__(self, lonir):
        self.lonir = lonir
    
    @commands.command()
    @commands.is_owner()
    async def sql(self, ctx: commands.Context, *command):
        command = ' '.join(command)
        status='OK'
        output = None
        try:
            output = database.database(command, 'all')
        except psycopg2.ProgrammingError as error:
            status = error
            
        embed = discord.Embed(
            title='SQL',
            description=command,
            colour=discord.Colour.from_rgb(0, 0, 0)
        )
        embed.add_field(name='Вывод', value=output, inline=False)
        embed.add_field(name='Состояние', value=status, inline=False)

        await ctx.send(embed=embed)
    
    @commands.command()
    @commands.is_owner()
    async def database_update(self, ctx: commands.Context):
        guilds = 0
        members = 0
        for guild in self.lonir.guilds:
            guild_id = database.database(f'''SELECT id
            FROM guilds
            WHERE id = {guild.id}''', 'one')
            if guild_id == None:
                database.database(f'''INSERT INTO guilds (id)
                VALUES ({guild.id})''')
                await ctx.send(f'Гильдия {guild.name} (`{guild.id}`) была записана в БД')
                guilds += 1

            for member in guild.members:
                member_id = database.database(f'''SELECT id
                FROM users
                WHERE guild_id = {guild.id} AND id = {member.id}''', 'one')
                if member_id == None:
                    database.database(f'''INSERT INTO users (guild_id, id)
                    VALUES ({guild.id}, {member.id})''')
                    await ctx.send(f'Пользователь {member} (`{guild.id}`) из гильдии {guild.name} (`{guild.id}`) был записан в БД')
                    members += 1

        await ctx.send(f'Обновление БД завершено. Было записано: **{guilds} гильдий, {members} участников**')

def setup(lonir):
    lonir.add_cog(Owner(lonir))