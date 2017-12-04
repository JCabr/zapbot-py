import inspect

import discord
from functools import wraps
import importlib
from enum import Enum, unique
from collections import OrderedDict

from .commandparsing import CommandParser
from .command import Command

@unique
class _CommandParamType(Enum):

    DEFAULT = 0
    BOT = 1
    CONTEXT = 2
    AUTHOR = 3
    SERVER = 4


_param_keywords = \
    {
        "BOT": {"bot", "bot_info", "botinfo"},
        "CTX": {"ctx", "context", "contx"},
        "AUTHOR": {"author", "author_info", "authorinfo"},
        "SERVER": {"server", "server_info", "serverinfo"}
    }


class ZapBot(discord.Client):

    def __init__(self, *, token=None, prefixes=None, help_format=None, pm_help=False, owner=None, **options):

        super().__init__(**options)

        # TODO: load in bot data from config file.

        self.owner = "186898416415014912"

        # NOTE: Change this when updating bot to read from config
        self.token = token

        # Make prefixes a dict of sets
        # Base sets:
        # { ALL: {} }
        # { USER: {} }
        # { ADMIN: {} }
        self.prefixes = set()
        # NOTE: Change this when updating bot to read from config
        self.prefixes.update(prefixes if isinstance(prefixes, list) else [prefixes])

        self.modules = OrderedDict()

        self.commands = set()

        self.command_parser = CommandParser(self)

    async def __help_cmd(self, message: discord.Message, args=None):

        help_content = ""

        for cmd in self.commands:
            help_content += "`{0}`:\n\t{1}\n".format(cmd.name, cmd.desc)

        await self.say(message.channel, help_content)

    async def say(self, destination, content=None, *, tts=False, embed=None):

        await self.send_message(destination=destination, content=content, tts=tts, embed=None)

    def add_module(self, cogs):

        def get_module_data(cogs):

            name = None
            cog_list = []

            if isinstance(cogs, dict):

                name = list(cogs.keys())[0]
                cog_list = []

                first_value = list(cogs.values())[0]

                if not isinstance(first_value, list):
                    cog_list.append(first_value)
                else:
                    cog_list.extend(first_value)

            elif isinstance(cogs, list):

                # Get name of the file for the first cog in the list.
                name = cogs[0].rsplit('.', 1)[-1]
                cog_list = cogs

            elif isinstance(cogs, str):

                name = cogs.rsplit('.', 1)[-1]
                cog_list = [cogs]

            return name, cog_list

        module_name, cog_list = get_module_data(cogs)

        self.modules[module_name] = cog_list

        for cog in cog_list:
            self.__add_cog(cog)

    # CRITICAL: Fix adding cogs
    def __add_cog(self, cog: str):

        mod = importlib.import_module(cog, package=None)  # type: module
        print(mod)
        members = inspect.getmembers(cog)

        commands = []

        for attr in dir(mod):

            attribute = getattr(mod, attr)

            if type(attribute) is Command:
                self.commands.add(attribute)

        for name, member in members:

            if type(member) is Command:

                if member.parent is None:
                    self.commands.add(member)

    def process_commands(self, message: discord.Message):

        if message.author.id != self.owner: return

        print(message.content)

        prefix = self.command_parser.determine_prefix(message.content)

        if prefix == message.content:
            print("Prefix is the only portion of the command")
            return

        if prefix:

            command_stack, command_args = self.command_parser.determine_command_structure(message.content, prefix)

            print(command_stack)
            print(command_args)