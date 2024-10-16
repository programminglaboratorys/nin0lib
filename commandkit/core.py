from .parser import eval_args

class PrefixError(Exception):
	""" raise when str doesn't starts with prefix(s) """

def get_word(self) -> str: # take whatever is the first word
	return str(self).split()[0]

def skip_prefix(string: str, prefix: str):
	""" skip prefix(s) if string doesn't starts with prefix(s) raise PrefixError() 
	if string equal prefix returns an empty string("") else remove the prefix
	"""
	if not string.startswith(prefix):
		raise PrefixError(f"the {repr(string)} doesn't start with prefix({repr(prefix)})")
	return string.removeprefix(prefix)

# Base.py
class CommandError(Exception):
	""" basic CommandError exception """

class InvaildCommandError(CommandError):
	""" when entered a command doesn't start with prefix or command is None or empty """


class CommandParser(object):
	""" to parse and """
	@staticmethod
	def parser(self, string: str):
		return str.split(string)
	
	def __init_subclass__(cls, parser=None, default_command_object=None) -> None:
		cls.parser = parser or cls.parser
		cls.default_command_object = default_command_object or cls.default_command_object

	def __init__(self, prefix: str, parser=None):
		super(CommandParser, self).__init__()
		if not isinstance(prefix,str):
			raise ValueError(f"excepted str but got ({repr(type(prefix).__name__)}) instead")
		if " " in self.prefix:
			raise PrefixError("prefix should not contain spaces")
		self.prefix = prefix
		self.parser = parser if parser is not None else self.parser

	def startswith_prefix(self, string: str):
		""" check if the input string start with prefix(s) """
		return string.startswith(self.prefix)

	def process_string(self, EA: list[str], string: str, allow_overflow:bool=True, **kw):
		if not self.startswith_prefix(string):
			raise InvaildCommandError(f"command must start with prefix({repr(self.prefix)})")
		args = skip_prefix(string.strip(), self.prefix)
		return eval_args(EA,self.split(args),allow_overflow=allow_overflow,**kw)

	def split(self, string: str):
		return self.parser(skip_prefix(string, self.prefix))

	def get_command_name(self, string: str):
		args = self.split(string)
		return args[0] if args else ""

	def get_command_args(self, string: str):
		args = self.split(string)[1::] # remove the command name
		return args
