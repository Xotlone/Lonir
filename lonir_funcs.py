import logging
import typing

from discord.ext import commands
from cogs import error_handler

log = logging.getLogger('logger')

async def get_member(ctx: commands.Context, member: typing.Union[int, str], is_expected: bool=True):
    member = str(member)
    try:
        member_id = int(''.join(list(filter(str.isdigit, member))))
    except ValueError:
        await error_handler.ErrorHandler.member_not_found(ctx)
    member = ctx.guild.get_member(member_id)
    if member == None and is_expected:
        await error_handler.ErrorHandler.member_not_found(ctx)
    else:
        return member

async def get_role(ctx: commands.Context, role: typing.Union[int, str], is_expected: bool=True):
    role = str(role)
    try:
        role_id = int(''.join(list(filter(str.isdigit, role))))
    except ValueError:
        await error_handler.ErrorHandler.role_not_found(ctx)
    role = ctx.guild.get_role(role_id)
    if role == None and is_expected:
        await error_handler.ErrorHandler.role_not_found(ctx)
    else:
        return role

async def time_decode(ctx: commands.Context, time_str: str):
    time_types = {
        'с': 1,
        'м': 60,
        'ч': 3600,
        'д': 86400
    }

    time_tokens = time_str.lower().split()
    t = 0
    for token in time_tokens:
        try:
            t += int(token[:-1]) * time_types[token[-1]]
        except ValueError:
            await error_handler.ErrorHandler.wrong_time_format(ctx)
    return t

class ProgressBar:
    def __init__(self, max_value, value=0, size=10, empty='●', full='█'):
        self.max_value = max_value
        self.value = value
        self.size = size
        self.empty = empty
        self.full = full
    
    def show(self):
        bar = ''
        procent = round(self.value / self.max_value * 100, 1)
        for i in range(self.size):
            if self.value >= (self.max_value / self.size) * i:
                bar += self.full
            else:
                bar += self.empty
        return {'bar': bar, 'procent': procent, 'val': self.value, 'max_val': self.max_value}