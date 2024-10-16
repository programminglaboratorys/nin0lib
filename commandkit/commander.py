from .core import CommandParser, CommandError, InvaildCommandError
from .parser import parse_annotation, parse_to_argv
from typing import Callable

import asyncio

class BadArgument(CommandError):
	""" when a parsing error on an argument to pass into a command """
	def __init__(self, message, parameters, command_object):
		super(BadArgument, self).__init__(message)
		self.parameters     = parameters
		self.command_object = command_object

class CommandNotFoundError(CommandError):
	""" when command doesn't exist """
	def __init__(self, message, name):
		super(CommandNotFoundError, self).__init__(message)
		self.name = name

class BasicCommand(object):
	function: Callable | asyncio.coroutine
	description: str | None
	data: dict
	name: str | None
	_command = lambda s,*args,**kw: type(s).command(*args,**kw)
	def __init__(self, function, description=None, name=None, **data):
		super(BasicCommand, self).__init__()
		self.function = function
		self.description = description
		self.data  = data
		self.name = name

	def command(*args, **kw):
		def inner(func):
			return BasicCommand(func,*args,**kw)
		return inner

	def __call__(self,*args,**kw):
		""" call self.function """
		return self.function(*args,**kw)

	async def __await__(self,*args,**kw):
		""" await self.function """
		return await self.function(*args,**kw)

	def __str__(self):
		""" return self.name or self.function.__name__ """
		return self.name if self.name else self.function.__name__

	def __eq__(self, other):
		if not isinstance(other, BasicCommand):
			raise TypeError(f"object of type '{type(other).__name__}' is not supported")
		return self.function == other.function

	def __hash__(self):
		return hash(self.function)

	def __repr__(self):
		return f"{type(self).__name__}({self.function.__name__}{':'+self.description if self.description else ''})"


class BasicCommands(object):
	default_command_object = BasicCommand
	def get_name_or_callable_name(self,name: Callable | str):
		if (not callable(name)) and (not isinstance(name,str)):
			raise ValueError(f"excepted str/function but got ({repr(type(name).__name__)}) instead")
		if callable(name):
			name = name.__name__
		return name

	def __init__(self):
		self.commands  =  {}

	def add_command(self, function: Callable, name:str=None, description:str=None, data:dict={}, **kw):
		""" add a new command """
		name = name if name is not None else function.__name__
		command_object = kw.get("Command",self.default_command_object)\
								(function, description, name, **data)  if not isinstance(function,BasicCommand) \
																	else function
		for ali in kw.get("aliases",[name]):
			self.commands[ali] = command_object
		return command_object

	def remove_command(self,name: Callable | str):
		""" remove a command """
		name = self.get_name_or_callable_name(name)
		if name in self.commands:
			del self.commands[name]
		return

	def command_exist(self,name: str):
		""" name(s) in commands """
		return name in self.commands

	def get_command(self, name: Callable | str):
		""" get command function raise CommandNotFoundError if command not in self.commands """ 
		if self.command_exist(name):
			return self.commands[self.get_name_or_callable_name(name)]
		else:
			raise CommandNotFoundError(f"command {repr(name)} do not exists", name)


	def call_command(self,name: Callable | str, *args, **kw):
		""" call command(s) """
		return self.get_command(name)(*args, **kw)

	def command(self,*args,**kw):
		def wrapper(function):
			return self.add_command(function, *args, **kw)
		return wrapper

	def __call__(self,name: Callable | str, *args, **kw):
		""" call command(s) """
		return self.call_command(name,*args,**kw)

	async def __await__(self,name: Callable | str,*args,**kw):
		""" await command(s) """
		return await self.function(*args,**kw)

	def __repr__(self):
		return f"{type(self).__name__}({list(self.commands.keys())})"


class Command(BasicCommand):
	parse_annotation = lambda s,*a,**k: parse_annotation(s.function,*a,**k)
	def command(*args, **kw):
		""" create a command object if inner is called """
		def inner(func):
			""" return command object when called """
			return Command(func,*args,**kw)
		return inner

	def _parse(self,*_args,**_kw):
		try:
			args, kw = self.parse_annotation(*_args,**_kw)
		except Exception as error:
			raise BadArgument("bad argument", (_args,_kw), self) from error
		return args,kw

	def __call__(self,*_args,**_kw):
		""" call self.function """
		args,kw = self._parse(*_args,**_kw)
		return self.function(*args,**kw)

	async def __await__(self,*_args,**_kw):
		""" await self.function """
		args,kw = self._parse(*_args,**_kw)
		return await self.function(*args,**kw)

class Commands(BasicCommands):
	default_command_object = Command

class Commander(Commands, CommandParser):
	def __init__(self, prefix:str):
		super(Commander,self).__init__()
		self.prefix = prefix

	def _process_command(self, string: str):
		""" return command, name """
		cmd = self.get_command_name(string)
		if not cmd:
			raise InvaildCommandError(f"Invalid command {repr(cmd)}")
		command = self.get_command(cmd)
		return command, cmd

	def process_command(self, string: str, **kw):
		command,_ = self._process_command(string)
		args = kw.get('lex',self.get_command_args)(string)
		return command(*args)

class CommandLine(Commands):
	""" works like Commander but convert string to argv """
	parse_to_argv = lambda s,string: parse_to_argv(string)
	def process_command(self, string: str, **kw):
		""" processing string to a command """
		argv = self.parse_to_argv(string)
		if not argv:
			raise InvaildCommandError(f"Invalid command") # to tell the user the command is empty
		command = self.get_command(argv[0])
		args = argv[1::] # remove the command name
		return command(*args)




"""
examples of 
>>> cmds = CommandLine()
>>> @cmds.command()
... def hello(name):
...     print("Hello,",name)
>>> cmds('hello',"World!") # or cmds('hello',name="World!")
Hello, World!
"""

"""
>>> cmds = Commander(prefix="?")
>>> @cmds.command()
... def hello(name):
...     print("Hello,",name)
...
>>> cmds.process_command('?hello World!')
Hello, World!
"""