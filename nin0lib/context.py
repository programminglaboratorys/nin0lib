from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Callable

from .message import Message, User
from .bot import Client

@dataclass
class Context(Message):
	send: Client.send
	command: str = field(default_factory=str)
	args: List[str] = field(default_factory=list)
	kwargs: Dict[str, Any] = field(default_factory=dict)

	def set_arguments(self, args: list, kwargs: dict):
		self.args = args
		self.kwargs = kwargs

	@classmethod
	def from_dict(cls, data: Dict[str, Any]):
		data = data.copy()
		data["author"] = data["userInfo"] if isinstance(data["userInfo"], User) else User(**data["userInfo"]) 
		del data["userInfo"]
		return cls(send=data.pop('send', Client.send), **data)

	@classmethod
	def create_context(cls, client: Client, message: Message):
		return cls(send=client.send, **asdict(message))
	
	def __repr__(self) -> str:
		return f"{self.__class__.__name__}(content={repr(self.content)}, id={self.id}, author={self.author})"

