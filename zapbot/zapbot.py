import discord
from functools import wraps
import importlib
from enum import Enum, unique


@unique
class _CommandParamType(Enum):

    DEFAULT = 0
    BOT = 1
    CONTEXT = 2
    AUTHOR = 3
    SERVER = 4


class ZapBot(discord.Client):

    def __init__(self, prefixes=None, help_format=None, pm_help=False, owner=None, **options):

        super.__init__(**options)

        # TODO: load in bot data from config file.

        # Make prefixes a dict of sets
        # Base sets:
        # { ALL: {} }
        # { USER: {} }
        # { ADMIN: {} }
        self.prefixes = dict()
        self.prefixes.add()
        self.cogs = []  # type: list