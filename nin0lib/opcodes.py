from enum import IntEnum
from dataclasses import dataclass, asdict
import json

class Opcodes(IntEnum):
    MESSAGE = 0
    LOGIN = 1
    HEARTBEAT = 2
    MESSAGE_HISTORY = 3
    ERROR = -1

@dataclass
class Packet:
    op: Opcodes
    d: dict

    def __post_init__(self):
        if not isinstance(self.op, (Opcodes,int)):
            raise TypeError("op must be int or Opcodes enum member")
        if isinstance(self.op, int):
            self.op = Opcodes(self.op)
    
    def to_json(self):
        packet: Packet = asdict(self)
        packet["op"] = int(packet["op"])
        return json.dumps(packet)

    @classmethod
    def from_json(cls, string: str):
        return cls(**json.loads(string))
