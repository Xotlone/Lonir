import logging, time

import discord
from discord.ext import commands
from discord_slash import cog_ext
from discord_slash.model import ButtonStyle
from discord_slash.utils import manage_components

from config import CONSTANTS, cmds
import lonir_funcs

log = logging.getLogger('logger')

class Useful(commands.Cog):
    def __init__(self, lonir):
        self.lonir = lonir
    
    @cog_ext.cog_slash(**cmds.COMMANDS('calculator').to_slash())
    @commands.cooldown(CONSTANTS.COOLDOWN_RATE, CONSTANTS.COOLDOWN_TIME)
    async def calculator(self, ctx: commands.Context, **kwargs):
        if kwargs != {}:
            primer = kwargs['пример']
        else:
            raise commands.errors.MissingRequiredArgument('Primer for calculator')

        embed = discord.Embed(
            title='Математический пример',
            description=f'{primer} = {eval(primer)}',
            colour=discord.Colour.from_rgb(*CONSTANTS.CLR)
        )
        await ctx.reply(embed=embed)

    @cog_ext.cog_slash(**cmds.COMMANDS('voting').to_slash())
    @commands.cooldown(CONSTANTS.COOLDOWN_RATE, CONSTANTS.COOLDOWN_TIME)
    async def voting(self, ctx: commands.Context, **kwargs):
        description = kwargs['описание'] + '\n'
        t = time.time() + await lonir_funcs.time_decode(ctx, kwargs['время'])
        start_t = time.strftime('%d.%m.%Y %H:%M', time.gmtime(time.time()))
        objects = [i for i in list(kwargs.values())[2:]]
        if len(objects) < 2:
            raise commands.errors.MissingRequiredArgument('Objects in voting')
        vals = {i: lonir_funcs.ProgressBar(1) for i in objects}
        voted_members = {}

        components = {}
        full_description = description + '\n'
        for i, obj in enumerate(objects):
            bar, procent, val, max_val = vals[obj].show().values()
            full_description += f'{i}.{obj} {bar} {val}/{max_val} {procent}%\n'
            components[obj] = manage_components.create_button(ButtonStyle.blue, obj)
        action_row = manage_components.create_actionrow(*list(components.values()))

        embed = discord.Embed(
            title='Голосование',
            description=full_description,
            colour=discord.Colour.from_rgb(*CONSTANTS.CLR)
        )
        embed.set_footer(text=f'Время на голосование: {kwargs["время"]}. Начало {start_t}')
        message = await ctx.send(embed=embed, components=[action_row])

        while True:
            if time.time() >= t:
                full_description = description + '\n'
                invert_vals = {v: k for k, v in vals.items()}
                vals = {k: v for v, k in sorted(invert_vals.items(), key=lambda val: val[0].value, reverse=True)}
                scores_sum = sum(map(lambda val: val[1].value, vals.items()))
                for value in vals:
                    vals[value].max_val = scores_sum
                
                for i, value in enumerate(vals):
                    bar, procent, val, max_val = vals[value].show().values()
                    if i == 0:
                        full_description += f'**{i}.{value} {bar} {val}/{max_val} {procent}%\n**'
                    else:
                        full_description += f'{i}.{value} {bar} {val}/{max_val} {procent}%\n'
                
                embed = discord.Embed(
                    title='Голосование окончено',
                    description=full_description,
                    colour=discord.Colour.green()
                )
                end_time = time.strftime('%d.%m.%Y %H:%M', time.gmtime(time.time()))
                embed.set_footer(text=f'Время на голосование: {kwargs["время"]}. Конец {end_time}')
                await message.edit(embed=embed, components=None)
                break

            is_clicked = await manage_components.wait_for_component(self.lonir, components=action_row)
            if is_clicked.channel == ctx.channel:
                for i, obj in enumerate(objects):
                    if is_clicked.component['label'] == obj:
                        event_author = is_clicked.author.id
                        if event_author in voted_members:
                            if voted_members[event_author] == obj:
                                del voted_members[event_author]
                                vals[obj].value -= 1
                            else:
                                vals[voted_members[event_author]].value -= 1
                                voted_members[event_author] = obj
                                vals[obj].value += 1 
                        else:
                            voted_members[event_author] = obj
                            vals[obj].value += 1
                        
                        full_description = description + '\n'
                        invert_vals = {v: k for k, v in vals.items()}
                        vals = {k: v for v, k in sorted(invert_vals.items(), key=lambda val: val[0].value, reverse=True)}
                        scores_sum = sum(map(lambda val: val[1].value, vals.items()))
                        for value in vals:
                            vals[value].max_val = scores_sum
                        
                        for i, value in enumerate(vals):
                            bar, procent, val, max_val = vals[value].show().values()
                            full_description += f'{i}.{value} {bar} {val}/{max_val} {procent}%\n'
                        
                        embed = discord.Embed(
                            title='Голосование',
                            description=full_description,
                            colour=discord.Colour.from_rgb(*CONSTANTS.CLR)
                        )
                        embed.set_footer(text=f'Время на голосование: {kwargs["время"]}. Начало {start_t}')
                        await is_clicked.edit_origin(embed=embed)

def setup(lonir):
    lonir.add_cog(Useful(lonir))