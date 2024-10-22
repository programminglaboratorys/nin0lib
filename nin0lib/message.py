from dataclasses import dataclass
from typing import Literal
from .roles import Roles, get_roles_from_int

@dataclass
class User:
	username: str
	roles: list[Roles]
	id: int
	bridgeMetadata: dict

	def __post_init__(self):
		if not isinstance(self.roles, (int, list)):
			raise TypeError("roles must be int or list")
		self.roles = get_roles_from_int(self.roles) if isinstance(self.roles, int) else self.roles
		self.id = int(self.id)
	
	@property
	def bot(self):
		""" Whether the user is a bot. """
		return Roles.BOT in self.roles

	def __repr__(self):
		return f"{self.__class__.__name__}(username={repr(self.username)}, roles={self.roles}, id={self.id})"

@dataclass
class Message:
	author: User
	timestamp: int
	content: str
	id: int
	device: Literal["web", "mobile", "bot"]|None
	type: int

	def __post_init__(self):
		self.author = User(**self.author) if isinstance(self.author, dict) else self.author
		self.id = int(self.id)

	@classmethod
	def from_dict(cls, data: dict):
		data = data.copy()
		data["author"] = data["userInfo"]
		data.pop("userInfo")
		return cls(**data)

	def __repr__(self) -> str:
		return f"{self.__class__.__name__}(author={self.author}, content={repr(self.content)}, id={self.id})"



