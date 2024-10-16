from ._parser import parse_to_argv
from itertools import zip_longest
from inspect import _POSITIONAL_ONLY,\
				_POSITIONAL_OR_KEYWORD,_KEYWORD_ONLY, signature


__all__ = ["Missing", "EAError", "EAOverflowError", "MissingError", "eval_args", "parse_annotation"]

Missing = type('Missing', (object,), {'__repr__': lambda s: "Missing"})() # creating a new type. thanks to: stackoverflow.com/questions/1528932/how-to-create-inline-objects-with-properties > https://stackoverflow.com/a/1528993


class EAError(Exception):
	""" basic exception for Eval args """

class EAOverflowError(OverflowError,EAError):
	""" when eval_args have more args to handle than what it can handle """
	def __init__(self, message: str, args: list, variables: dict, expexcted_lenght: int):
		super(EAOverflowError,self).__init__(message)
		self.expexcted_lenght = expexcted_lenght
		self.args = args
		self.variables = variables

class MissingError(EAError):
	""" when argument(s) is missing """
	def __init__(self, message: str, args: list, variables: dict, names: list):
		super(MissingError,self).__init__(message)
		self.names = names
		self.args = args
		self.variables = variables


def eval_args(EA:list, args:list, allow_overflow:bool=False, Missing_okay:bool=True, Missing:any=Missing):
	"""
	example:
	eval_args(["whatup","hmm","*","hehe"],"good ye? more stuff :)".split()) -> \
	({'whatup': 'good', 'hmm': 'ye?', 'hehe': ['more', 'stuff', ':)']}, [])
	"""
	# tuple(zip(*enumerate(EA))) -> ((0, 1, 2, 3), ('whatup', 'hmm', '*', 'hehe'))
	# zip(*tuple(zip(*enumerate(EA))),args) -> [(0, 'whatup', 'good'), (1, 'hmm', 'ye?'), (2, '*', 'more'), (3, 'hehe', 'stuff')]
	# dict(list(zip(EA,args))) -> {'whatup': 'good', 'hmm': 'ye?', 'hehe': 'stuff'}
	star = False # turns True when reached to the keyword arguments (e.g ["*","kw"])
	variables = {}
	for index, argname, item in zip_longest(*zip(*enumerate(EA)),args.copy(),fillvalue=Missing):
		if argname is Missing: # when the argname is missing
			break
		elif star:
			li = args[len(variables)::]
			variables[argname] = li
			for _ in range(len(args)):
				del args[0]
			break
		if argname == "*":
			star = True
			if   index == len(EA)-1:
				raise ValueError("excepted an argument name after '*'")
			continue
		else:
			variables[argname] = item
			if item is not Missing: # avoid index error
				del args[0]

	if (not Missing_okay) and Missing in variables.values():
		names = [repr(key) for key,value in variables.items() if value is Missing]
		raise  MissingError(f"missing {len(names)} required {'arguments' if len(names) > 1 else 'argument'}: {', '.join(names)}", args, variables, names = names)

	if args and not allow_overflow: # there  is still args in
		lenght = (len(args)-1 if "*" not in args else len(args)-2) # expexcted lenght
		raise EAOverflowError(f"takes {lenght} argument but {len(args)} were given", args, variables, expexcted_lenght=lenght)

	return variables,args # return , the overflowed arguments

def parse_annotation(f, *_args, **_kw):
	sign = signature(f)
	params = sign.parameters.values()
	return _parse_annotation(params,*_args,**_kw)

def _parse_annotation(params, *_args, **_kw):
	if not list(params): # if params is empty
		return _args,_kw
	args = []
	kw = {} | _kw
	for index,param in enumerate(params):
		try:
			item = _args[index]
		except IndexError:
			if param.kind in [_KEYWORD_ONLY,_POSITIONAL_OR_KEYWORD] and param.name in _kw:
				if param.annotation is not param.empty:
					kw[param.name] = param.annotation(_kw[param.name])
				else:
					kw[param.name] = _kw[param.name]
			continue
		if param.kind in [_POSITIONAL_ONLY,_POSITIONAL_OR_KEYWORD]:
			if param.annotation is not param.empty:
				args.append(param.annotation(item))
			else:
				args.append(item)
		elif param.kind is param.VAR_POSITIONAL:
			for item in _args[index::]:
				if param.annotation is not param.empty:
					args.append(param.annotation(item))
				else:
					args.append(item)
			break
		if param.kind in [_KEYWORD_ONLY,_POSITIONAL_OR_KEYWORD] and param.name in _kw:
			if param.annotation is not param.empty:
				kw[param.name] = param.annotation(_kw[param.name])
			else:
				kw[param.name] = _kw[param.name]
	return args,kw
