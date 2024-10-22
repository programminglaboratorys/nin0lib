from enum import Enum

class Roles(Enum):
    GUEST = 1 << 0
    USER = 1 << 1
    BOT = 1 << 2
    SYSTEM = 1 << 3
    MOD = 1 << 4
    ADMIN = 1 << 5

def get_roles_from_int(value):
    return [role for role in Roles if value & role.value]