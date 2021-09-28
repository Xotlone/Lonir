import logging

import discord
from discord.ext import commands

from config import CONSTANTS

log = logging.getLogger('logger')

class ErrorMessage:
    def __init__(self, title: str, description: str='', colour: discord.Colour=discord.Colour.red()):
        self.title = title
        self.description = description
        self.colour = colour
    
    def embed(self):
        return discord.Embed(
            title=self.title,
            description=self.description,
            colour=self.colour
        )

class ErrorHandler(commands.Cog):
    def __init__(self, lonir):
        self.lonir = lonir

    @staticmethod
    async def member_not_found(ctx: commands.Context):
        message = ErrorMessage('Не могу найти такого участника').embed()
        await ctx.reply(embed=message)
        raise Exception('Member not found')
    
    @staticmethod
    async def role_not_found(ctx: commands.Context):
        message = ErrorMessage('Не могу найти такую роль').embed()
        await ctx.reply(embed=message)
        raise Exception('Member not found')
    
    @staticmethod
    async def wrong_time_format(ctx: commands.Context):
        message = ErrorMessage('Неверный формат времени').embed()
        await ctx.reply(embed=message)
        raise Exception('Wrong time format')

    @commands.Cog.listener()
    async def on_error(self, ctx: commands.Context, error: commands.CommandError):
        log.error(error)

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):
        log.error(error)
        message = None

        try:
            if isinstance(error, commands.errors.CommandOnCooldown()):
                message = ErrorMessage('Задержка между командами', f'Повторите через {error.retry_after} с.')
            
            elif isinstance(error, commands.errors.CommandNotFound):
                message = ErrorMessage('Неизвестная команда')
            
            elif isinstance(error, commands.errors.NSFWChannelRequired):
                message = ErrorMessage('Не NSFW канал')

            elif isinstance(error, commands.errors.MissingRequiredArgument):
                message = ErrorMessage(f'Нет аргумента {error.param.name}')
            
            elif isinstance(error, discord.errors.HTTPException):
                log.warn('!!! Rate limit !!!')
        except TypeError:
            pass
        except Exception as e:
            message = e
        finally:
            if message != None:
                await ctx.reply(embed=message.embed())

def setup(lonir):
    lonir.add_cog(ErrorHandler(lonir))