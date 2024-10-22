# Roles

The [Roles](https://github.com/programminglaboratorys/nin0lib/blob/main/nin0lib/roles.py#L3) a enum represents different roles that a user can have in chat.

## Enum Values

### `GUEST`

The `GUEST` role represents a guest user.

### `USER`

The `USER` role represents a regular user.

### `BOT`

The `BOT` role represents a bot user.

### `SYSTEM`

The `SYSTEM` role represents system.

### `MOD`

The `MOD` role represents a moderator.

### `ADMIN`

The `ADMIN` role represents an administrator.

## Function: [get_roles_from_int](https://github.com/programminglaboratorys/nin0lib/blob/main/nin0lib/roles.py#L11)

The [get_roles_from_int](https://github.com/programminglaboratorys/nin0lib/blob/main/nin0lib/roles.py#L11) function takes an integer value and returns a list of [Roles](https://github.com/programminglaboratorys/nin0lib/blob/main/nin0lib/roles.py#L3) objects that correspond to the roles represented by the integer value.

```python
from nin0lib.roles import get_roles_from_int

roles = get_roles_from_int(6)  # Returns [<Roles.USER: 2>, <Roles.BOT: 4>]
```
