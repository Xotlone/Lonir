import typing

from discord import Permissions
from discord_slash import SlashCommandOptionType
from discord_slash.utils import manage_commands

general_permissions = Permissions.general()

class Cmd:
    def __init__(
        self,
        name: str,
        desc: str,
        options: typing.List[typing.Dict]=None,
        permissions: Permissions=general_permissions,
        nsfw: bool=False
    ):
        self.name = name
        self.desc = desc
        self.options = options
        self.permissions = permissions
        self.nsfw = nsfw

    def to_slash(self):
        out = {
            'name': self.name,
            'description': self.desc,
            'options': self.options
        }
        return out

class Category:
    def __init__(
        self,
        name: str,
        desc: str,
        commands: typing.List[Cmd]
    ):
        self.name = name
        self.desc = desc
        self.commands = commands

class Commands:
    commands = []

    def __init__(self, *categories: Category):
        self.categories = categories
        for category in categories:
            for command in category.commands:
                Commands.commands.append(command)
    
    def __call__(self, name: str) -> typing.Union[Category, Cmd]:
        self.name = name.lower()
        for category in self.categories:
            if category.name.lower() == name:
                return category
            
            for cmd in category.commands:
                if cmd.name.lower() == name:
                    return cmd
        
        raise ValueError(f'Command or category {name} not found')
    
    def sort(self) -> None:
        for i in range(len(self.categories)):
            self.categories[i].commands = sorted(self.categories[i].commands, key=lambda cmd: cmd.name)

            for j in range(len(self.categories[i].commands)):
                for k in range(len(self.categories[i].commands[j].options)):
                    self.categories[i].commands[j].options[k].choices_sort()

COMMANDS = Commands(
    Category(
        'Базовые команды',
        'Стандартный набор команд',
        [
            Cmd(
                'help',
                'Я покажу вам список команд или расскажу про команду',
                [
                    manage_commands.create_option(
                        'команда',
                        'Впишите сюда команду или категорию, что-бы узнать больше',
                        SlashCommandOptionType.STRING,
                        False
                    )
                ]
            ),
            Cmd(
                'ping',
                'Моя задержка'
            ),
            Cmd(
                'avatar',
                'Аватар участника',
                [
                    manage_commands.create_option(
                        'участник',
                        'id или пинг участника',
                        SlashCommandOptionType.STRING,
                        False
                    )
                ]
            )
        ]
    ),
    Category(
        'Полезные команды',
        'Команды, которые могут пригодится в повседневности... Ну или не могут',
        [
            Cmd(
                'calculator',
                'Стандартный калькулятор',
                [
                    manage_commands.create_option(
                        'пример',
                        'Математический пример по типу "2+2"',
                        SlashCommandOptionType.STRING,
                        True
                    )
                ]
            ),
            Cmd(
                'voting',
                'Голосование',
                [
                    manage_commands.create_option(
                        'описание',
                        'Описание голосования. Пример "Лучший тип наушников"',
                        SlashCommandOptionType.STRING,
                        True
                    ),
                    manage_commands.create_option(
                        'время',
                        'Время, через которое будут опубликованиы результаты голосования. Пример "1ч 30м"',
                        SlashCommandOptionType.STRING,
                        True
                    ),
                    manage_commands.create_option(
                        'объект1',
                        'Первый объект голосования',
                        SlashCommandOptionType.STRING,
                        True
                    ),
                    manage_commands.create_option(
                        'объект2',
                        'Второй объект голосования',
                        SlashCommandOptionType.STRING,
                        True
                    ),
                    manage_commands.create_option(
                        'объект3',
                        'Третий объект голосования',
                        SlashCommandOptionType.STRING,
                        False
                    ),
                    manage_commands.create_option(
                        'объект4',
                        'Четвёртый объект голосования',
                        SlashCommandOptionType.STRING,
                        False
                    ),
                    manage_commands.create_option(
                        'объект5',
                        'Пятый объект голосования',
                        SlashCommandOptionType.STRING,
                        False
                    ),
                    manage_commands.create_option(
                        'объект6',
                        'Шестой объект голосования',
                        SlashCommandOptionType.STRING,
                        False
                    ),
                    manage_commands.create_option(
                        'объект7',
                        'Седьмой объект голосования',
                        SlashCommandOptionType.STRING,
                        False
                    ),
                    manage_commands.create_option(
                        'объект8',
                        'Восьмой объект голосования',
                        SlashCommandOptionType.STRING,
                        False
                    )
                ]
            )
        ]
    ),
    Category(
        'Информация',
        'Информация о участниках, сервере, обо мне',
        [
            Cmd(
                'info',
                'Информация о участнике',
                [
                    manage_commands.create_option(
                        'участник',
                        'id или пинг участника',
                        SlashCommandOptionType.STRING,
                        False
                    )
                ]
            )
        ]
    )
)