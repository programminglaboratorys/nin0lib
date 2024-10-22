# Message

The [`Message`](https://github.com/programminglaboratorys/nin0lib/blob/main/nin0lib/message.py#L26) is a dataclass; class represents a message sent by a user in a chat.

## Fields

### `author`: `User`

The user who sent the message.

### `timestamp`: `int`

The timestamp of when the message was sent.

### `content`: `str`

The content of the message.

### `id`: `int`

The unique ID of the message.

### `device`: `Literal["web", "mobile", "bot"] | None`

The device type that sent the message, or `None` if it's the system.

## Methods

### `from_dict(cls, data: dict)`

Creates a new `Message` object from a dictionary.

# User

The [`User`](https://github.com/programminglaboratorys/nin0lib/blob/main/nin0lib/message.py#L6) is a dataclass; class represents a user in chat.

## Fields

### `username`: `str`

The username of the user.

### roles: `list[Roles]`

The roles that the user has. type [`Roles`](https://github.com/programminglaboratorys/nin0lib/blob/main/nin0lib/roles.py#L3)

### `id`: `int`

The unique ID of the user.

### property `bot` -> bool

Returns whether the user is a bot.
