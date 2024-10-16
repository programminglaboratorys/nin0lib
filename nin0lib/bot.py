from commandkit import Commander, PrefixError, Command
from commandkit.parser import _parse_annotation
from inspect import signature

from dataclasses import dataclass

import asyncio

from .message import Message
from .client import Client


class BotCommand(Command):
	def parse_annotation(s,*_args,**_kw):
		sign = signature(s.function)
		params = list(sign.parameters.values())[1::]
		return _parse_annotation(params,*_args,**_kw)

class CommandsManager(Commander):
	default_command_object = BotCommand
	async def process_command(self, context: "Context", string: str, **kw):
		try:
			command,_ = self._process_command(string)
		except PrefixError:
			return
		args = kw.get('lex',self.get_command_args)(string)
		return await command(context, *args)

class Bot(Client, CommandsManager):
    def __init__(self, *, prefix, **kw):
        Client.__init__(self, **kw)
        CommandsManager.__init__(self, prefix=prefix)
        if kw.get("default_help_command") == None:
            async def default_help(context):
                showed = set()
                commands_list = "```commands:\n"
                for command in self.commands.values():
                    if command in showed:
                        continue
                    commands_list += f"\t- {command.name}" +  (f" | {command.description}\n" if command.description and command.description.strip() else "\n")
                    showed.add(command)
                commands_list += "```"
                await context.send(commands_list)
            self.add_command(default_help, "help", "shows this help message")
        return
    async def on_message(self, message: Message):
        asyncio.create_task(self.process_command(create_context(self, message), message.content))
    

@dataclass
class Context:
    role: int
    content: str
    username: str
    send: Bot.send


def create_context(bot: Bot, message: Message):
    return Context(role=message.role, content=message.content, username=message.username, send=bot.send)