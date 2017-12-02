import discord
from typing import Callable


class Command:

    def __init__(self, name: str, func: Callable, desc: str = None, static_typing: bool = True):

        self.name = name
        self.func = func
        self.desc = desc
        self.parent = None
        self.children = []
        self.static_typing = static_typing

    def __str__(self):

        return f"COMMAND NAME: {self.name}\n" \
               f"CMD FUNC NAME: {self.func.__name__}\n" \
               f"DESC: {self.desc}\n" \
               f"TYPING: {'STATIC' if self.static_typing else 'DYNAMIC'}"


class CommandSettings:

    def __init__(self, *, name: str = None, func: Callable = None, desc: str = None, static_typing: bool = True):

        self.name = name
        self.func = func
        self.desc = desc
        self.static_typing = static_typing
