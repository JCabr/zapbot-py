<p align="left">
  <a title="License"><img src="https://img.shields.io/badge/License-MIT-blue.svg?style=flat-square"></a>
</p>

[comment]: # ( Logo will be unhidden after a more stable version is reached, and there is more reason to have presentation.<p align="center"><a title="ZapBotLogo"> <img src="https://i.imgur.com/uyYlhIX.png" width="400"/></a></p> )

<p align="center">
  <a title="PythonVersion" href="https://www.python.org/downloads/release/python-350/"><img src="https://img.shields.io/badge/Python-3.5.0-blue.svg?style=flat-square"></a>
  <a title="DiscordPyVersion" href="https://github.com/Rapptz/discord.py"><img src="https://img.shields.io/badge/Discord.py-0.16.12-738bd7.svg?style=flat-square"></a>
  <a title="FrameworkVersion"><img src="https://img.shields.io/badge/ZAP%20Framework-0.3.0a-23272A.svg?style=flat-square&logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAFoAAABZCAMAAACJ4sOeAAAADFBMVEUAAAAjJyr4%2BfkkKCufxc3OAAAAAXRSTlMAQObYZgAAAQJJREFUeAHt2EEKwzAQxdCovf%2Bdu9SqQ0M0kEB1gGcwGMw%2FzgTHUgB7MuzJsCdDL1svWys%2F0mbPZs9mzcasl61HrZetl62XrZdtRdYOuj%2F9WqLfYBbQcJIml6XJZWlyWZpcliaXpallaYhl6dHmKk0qSw82BU0mSw82FU0iSw82JU0kS2PK1DTKOU3ywR0IYlqDLVo7p79fFBfzzJJWloloZZ2AVtZuaGWraGWraGWraEVr6B82oErWlo5kbelGNqQj2aQr2aQr2aQr2aQr2aQr2aRD2S4Af%2FpOK04vWy9bL1sv24Qqp%2FZRxOPfjnTVIr1q97L1svWy9bIp9yn3Kfedkz%2Bz1g27UbBJ0gAAAABJRU5ErkJggg%3D%3D"></a>
</p>

[comment]: # ( Bot list will be unhidden after they are converted to ZapBot code.<p align="center"><a title="NumBots"><img src="https://img.shields.io/badge/%23%20Bots-2-000000.svg?style=flat-square"></a><a title="NZAPBot"><img src="https://img.shields.io/badge/N--ZAP%20'17-0.1.9b-0AFC15.svg?style=flat-square"></a><a title="LunaBot"><img src="https://img.shields.io/badge/Luna%20N--I/O-0.2.3b-d25b63.svg?style=flat-square"></a></p>)

ZapBot is a framework that aims to help automate the basics for setting up the workings of a Discord bot and providing a library of code to use that is helpful for very common situations when writing larger, flexible bots with nice presentation, while offering enough flexibility in customizing what it does to remove any annoying limitations that could come from using a framework compared to writing the bot code from scratch.

The goal is to have a framework that makes it much easier for you write a bot that works how you want it to, without having to wrestle around with the framework to even have it working how you want it.

## Features (Planned for v1.0)

### Flexible Configuration

Use a simple YAML config file to set the bot up with: 
- Commands
- User types
	- i.e., types of users like "mod", "admin", "DJ", etc.
- Command prefixes (general and/or user type specific)
- General settings
	- Such as whether to default to checking if command arguments match what's given in type hints for command functions.

Here is an some example YAML that will create a bot that:
- Has a system for different permissions for regular users, moderators, and administrators.
	- Admins have all permissions, and correspond to everyone with "administrator" permission in a server.
- Has separate prefixes for each permission level.
- Can easily be set up to have separate help commands for each permission level.
- Does *not* require that command arguments match with the type hints in a command function (at least without setting a command to work otherwise).
- Automatically loads in every command from the supplied python modules.
```yaml
bot info:
  token: "<bot token here>"
  prefixes:					# You can list prefixes for normal user commands
    user:					# and admin commands here, or in the
      - "b!"					# "user types" section
    admin:
      - "b@"

user types:
  mod:
    prefix: "b:"
    role:
      name: "Moderator"
  admin:
    inherits from:				# This gives admins access to everything mods
      - mod					# have access to

cogs:
  Fun:
    - cogs.fun  				# For this example there is a file "cogs/fun.py"
  Misc:
    - cogs.random				# Cogs can be composed of multiple modules
    - cogs.joke_stuff

bot defaults:
  typing is enforced: no
```

### Simple Command Creation

Simple, yet flexible method of creating command functions for the bot.
- Bot will be smart about seeing what the programmer wants for the command, looking at the context of the function and its parameters to give what you want.
- Equally simple method for making subcommands (nested as deep as you want)

Some example code for how a simple command and subcommand is created:

```py
import zapbot

@zapbot.command()
async def hello(bot, author, context):
  if not context.called_subcommands:
    await bot.say(f"Hello, {author}!")
    
@hello.subcommand()
async def to(bot, member):
  await bot.say(f"Hello, {member.mention}!")
```
(*That's all it takes, other than listing the module with the commands in the bot config file.*
*Note that only the `member` argument is supplied by a discord member, everything else will be filled in with the wanted information by the bot.*)

### First-Class Help Commands

Help Commands, while naturally a bit different than normal commands, work very similarly to how regular commands do, and this includes their creation and modification.
- Write help commands very easily.
	- Essentially the same process as writing a normal command.
- Easily have separate help functions for different user types (such as having one for normal commands, and one for admin commands).
	- The bot gives easy access to its list of cogs, commands, and everything you would want when writing a help command.

Some example code for writing a simple set of help commands:
```py
import zapbot

bot = ZapBot()

@bot.help_command()
async def user_help_command(bot):
  # Example help command to show how simple it can be
  help_menu = ""
  
  for module_name, module in bot.modules.items():
    # Add header for module that is bolded and underlined.
    help_menu += f"\n**__{module_name}__**\n"
    # Add list of commands that are in monospaced text and separated by commas.
    help_menu += ", ".join(f"`{command_name}`" for command_name in module.commands.keys()) + "\n"
  
  await bot.embed_reply(title="Help Menu", desc=help_menu, color=bot.bot_color)
    
@bot.help_command(type="admin")
async def admin_help_command(bot):
  # Other help command here
```
(*Note that everything you would want consistently ordered when writing a help command is ordered, either as a list or OrderedDict*)

### Flexible, Helpful Library
ZapBot aims to also come with a library of helpful features with the goal to make it so you would only have to reach into the `discord.py` when you need to.
- Functionality for a special kind of string interpolation that allows programmers to write strings containing Discord data (members, channels, roles, etc.) without having to write any code to get each piece of data.
	- So no having to repeatedly write `discord.utils.get()`
- A library of things generally useful when making Discord bots.
	- Help for working with colors, embeds, etc.
