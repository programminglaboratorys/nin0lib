from commandkit import Commander, BasicCommand

import asyncio


from .message import Message
from .client import Client
from .view import StringView
from .context import Context
from .roles import Roles

class BotCommand(BasicCommand):
	pass

class CommandsManager(Commander):
	default_command_object = BotCommand


	async def process_command(self, context: "Context", string: str, **kw):
		""" processing string to a command """
		view = StringView(string)
		if not view.skip_string(self.prefix):
			return
		name = view.get_word()
		if not name:
			return
		command: BotCommand = self.get_command(name)
		args, kw = parse_arguments(command.function, view)
		context.set_arguments(args, kw)
		context.command = name
		return await command(context, *args, **kw)

class Bot(Client, CommandsManager):
    def __init__(self, *, prefix, **kw):
        Client.__init__(self, **kw)
        CommandsManager.__init__(self, prefix=prefix)
        if kw.get("default_help_command") == None:
            async def default_help(context):
                showed = set()
                commands_list = "```commands:\n"
                for name, command in self.commands.items():
                    if command in showed:
                        continue
                    commands_list += f"\t- {name}" +  (f" | {command.description}\n" if command.description and command.description.strip() else "\n")
                    showed.add(command)
                commands_list += "```"
                await context.send(commands_list)
            self.add_command(default_help, "help", "shows this help message")
        return

    async def on_message(self, message: Message):
        if Roles.BOT in message.author.roles:
            return
        asyncio.create_task(self.process_command(Context.create_context(self, message), message.content))


from inspect import _POSITIONAL_ONLY,\
				_POSITIONAL_OR_KEYWORD, _KEYWORD_ONLY, _VAR_POSITIONAL, signature, Parameter


def run_converter(param: Parameter, value):
	if param.annotation is not param.empty:
		return param.annotation(value)
	return value

def parse_arguments(function, view: StringView):
	args = []
	kwargs = {}
	sign = signature(function)
	params = list(sign.parameters.values())[1::] # skip context object
	if not list(params): # if params is empty
		return args, kwargs
	for param in params:
		if param.kind in (_POSITIONAL_ONLY, _POSITIONAL_OR_KEYWORD):
			view.skip_ws()
			args.append(run_converter(param, view.get_word()))
		elif param.kind == _KEYWORD_ONLY:
			view.skip_ws()
			kwargs[param.name] = run_converter(param, view.read_rest())
		elif param.kind == _VAR_POSITIONAL:
			while not view.eof:
				if not view.skip_ws(): # if no white space was skipped
					break
				args.append(run_converter(param, view.get_word()))
		else:
			raise NotImplementedError("Unknown kind type {} for parameter {}. ({})".format(param.kind, param.name, function))
	return args, kwargs
