import logging

import discord
from discord.ext import commands
from discord_slash import cog_ext
from discord_slash.context import SlashContext

from config import CONSTANTS, cmds, database
import lonir_funcs

discord.Permissions.advanced()
log = logging.getLogger('logger')

class Information(commands.Cog):
    def __init__(self, lonir):
        self.lonir = lonir
    
    @cog_ext.cog_slash(**cmds.COMMANDS('info').to_slash())
    @commands.cooldown(CONSTANTS.COOLDOWN_RATE, CONSTANTS.COOLDOWN_TIME)
    async def info(self, ctx: SlashContext, **kwargs):
        if kwargs != {}:
            member = await lonir_funcs.get_member(ctx, kwargs['участник'])
        else:
            member = ctx.author
        
        embed = discord.Embed(
            title=f'Информация о {member.name}',
            description='Ниже - параметры участника: общие параметры Дискорд, роли, число очков в моей экономике и т.д.',
            colour=discord.Colour.from_rgb(*CONSTANTS.CLR)
        )
        embed.set_thumbnail(url=member.avatar_url)

        created = '{0.day}.{0.month}.{0.year} {0.hour}:{0.minute}'.format(member.created_at)
        joined = '{0.day}.{0.month}.{0.year} {0.hour}:{0.minute}'.format(member.joined_at)
        discord_params = f'''Бот — {'<:Y_:892513393787936868>' if member.bot else '<:N_:892513393787936868>'}
Существует с **{created}**
На сервере с **{joined}**
id — `{member.id}`
Роли — **{', '.join(map(lambda role: role.name, member.roles))}**'''
        embed.add_field(
            name='Параметры Дискорд',
            value=discord_params,
            inline=False
        )

        scores = database.database(f'''SELECT scores
        FROM users
        WHERE guild_id = {member.guild.id} AND id = {member.id}''', 'one')[0]
        level = CONSTANTS.SCORES_TO_LEVEL(scores)
        next_level_scores = CONSTANTS.LEVEL_UP(level + 1)
        local_range = next_level_scores - CONSTANTS.LEVEL_UP(level)
        local_scores = local_range - (next_level_scores - scores)
        print(local_range, local_scores)
        economy_bar = lonir_funcs.ProgressBar(local_range, local_scores, 25).show()
        economy_params = f'''Уровень — **{level}**
Очки — **{scores}/{next_level_scores} {economy_bar['procent']}%**
[{economy_bar['bar']}]'''
        embed.add_field(
            name='Экономика',
            value=economy_params,
            inline=False
        )
        
        await ctx.reply(embed=embed)

def setup(lonir):
    lonir.add_cog(Information(lonir))