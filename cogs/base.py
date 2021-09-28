import logging

import discord
from discord.ext import commands
from discord_slash import cog_ext, SlashContext

from config import CONSTANTS, cmds
import lonir_funcs

log = logging.getLogger('logger')

class Base(commands.Cog):
    def __init__(self, lonir):
        self.lonir = lonir
    
    @cog_ext.cog_slash(**cmds.COMMANDS('help').to_slash())
    @commands.cooldown(CONSTANTS.COOLDOWN_RATE, CONSTANTS.COOLDOWN_TIME)
    async def help(self, ctx: SlashContext, **kwargs):
        command_or_category = kwargs['команда'] if kwargs != {} else ''
        
        if command_or_category == '':
            embed = discord.Embed(
                title='Помощь',
                description='Список всех категорий с командами',
                colour=discord.Colour.from_rgb(*CONSTANTS.CLR)
            )
            for category in cmds.COMMANDS.categories:
                embed.add_field(name=category.name, value=', '.join(list(map(lambda x: f'`{x.name}`', category.commands))), inline=False)
            
            await ctx.reply(embed=embed)
        
        else:
            try:
                category_command = cmds.COMMANDS(command_or_category)
            except ValueError:
                raise commands.errors.CommandNotFound(f'Command or category {command_or_category} not found')
            
            if isinstance(category_command, cmds.Category):
                category = category_command
                description = f'''{category.desc}

Команды:
{', '.join(list(map(lambda command: f'`{command.nmae}`', category.commands)))}'''
                embed = discord.Embed(
                    title=category.name,
                    description=description,
                    colour=discord.Colour.from_rgb(*CONSTANTS.CLR)
                )
                await ctx.reply(embed=embed)
            
            elif isinstance(category_command, cmds.Cmd):
                command = category_command
                _access = 'общая'
                if command.permissions.administrator:
                    _access = 'администрация'
                elif command.permissions.ban_members:
                    _access = 'модерация'
                nsfw = '<:Y_:892513393787936868>' if command.nsfw else '<:N_:892513393787936868>'

                if command.options != None:
                    arguments = ' '.join(list(map(lambda option: f'{option["name"]}: ', command.options)))
                    syntax = f'`{command.name} {arguments}`'
                else:
                    syntax = f'`{command.name}`'
                description = f'''{command.desc}

Доступ: {_access}
NSFW: {nsfw}
Синтаксис: {syntax}'''
                embed = discord.Embed(
                    title=f'О команде {command.name}',
                    description=description,
                    colour=discord.Colour.from_rgb(*CONSTANTS.CLR)
                )
                await ctx.reply(embed=embed)
    
    @cog_ext.cog_slash(**cmds.COMMANDS('ping').to_slash())
    @commands.cooldown(CONSTANTS.COOLDOWN_RATE, CONSTANTS.COOLDOWN_TIME)
    async def ping(self, ctx: SlashContext):
        embed = discord.Embed(
            title=f'Задержка {round(self.lonir.latency, 1) * 100}ms.',
            colour=discord.Colour.from_rgb(*CONSTANTS.CLR)
        )
        await ctx.reply(embed=embed)
    
    @cog_ext.cog_slash(**cmds.COMMANDS('avatar').to_slash())
    @commands.cooldown(CONSTANTS.COOLDOWN_RATE, CONSTANTS.COOLDOWN_TIME)
    async def avatar(self, ctx: SlashContext, **kwargs):
        if kwargs != {}:
            member = await lonir_funcs.get_member(ctx, kwargs['участник'])
        else:
            member = ctx.author

        avatar = member.avatar_url
        embed = discord.Embed(
            title=f'Аватар {member.name}',
            colour=discord.Colour.from_rgb(*CONSTANTS.CLR)
        )
        embed.set_image(url=avatar)
        await ctx.reply(embed=embed)

def setup(lonir):
    lonir.add_cog(Base(lonir))