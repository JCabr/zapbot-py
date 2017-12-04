# from .zapbot import ZapBot
from ._custom_types.stack import Stack
from .command import Command

class CommandParser:

    def __init__(self, bot):

        self.bot = bot

    def determine_prefix(self, content: str):

        return next((prefix for prefix in self.bot.prefixes if content.startswith(prefix)), None)

    def determine_command_structure(self, content: str, found_prefix: str):

        command_pieces = content.lstrip(found_prefix).split()
        command_stack = Stack()
        args = []

        root_command = self.find_command(command_pieces[0], self.bot.commands)

        if root_command:

            command_stack.push(root_command)
            index = 1
            subcommand_found = True
            able_to_search_command = lambda: subcommand_found and index < len(command_pieces)

            while able_to_search_command():

                piece = command_pieces[index]
                subcommand = self.find_command(piece, command_stack.peek().children)

                subcommand_found = subcommand is not None

                if subcommand_found:
                    command_stack.push(subcommand)
                    index += 1

            if index < len(command_pieces):
                args = command_pieces[index: ]

        return command_stack, args

    # Finds the command from the list of commands that match the given name, if any (includes aliases).
    # If there are multiple matches, for whatever reason, only the first is considered.
    def find_command(self, command_name: str, command_list):

        matched_commands = [command for command in command_list if
                            command_name == command.name or command_name in command.aliases]

        return matched_commands[0] if matched_commands else None
