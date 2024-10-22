# Context

The [Context](https://github.com/programminglaboratorys/nin0lib/blob/main/nin0lib/context.py#L8) is a dataclass; class represents the context of a command execution.

## Inheritance

The `Context` class inherits from [`Message`](https://github.com/programminglaboratorys/nin0lib/blob/main/nin0lib.docs/message.md).

## Fields

### `send`: [`Client.send`](https://github.com/programminglaboratorys/nin0lib/blob/main/nin0lib.docs/client.md#sendself-message-str)

A function that sends a message to the chat.

### [command](https://github.com/programminglaboratorys/nin0lib/blob/main/nin0lib/bot.py#L30): `str`

The command that was executed.

### `args`: `List[str]`

The arguments passed to the command.

### `kwargs`: `Dict[str, Any]`

The keyword arguments passed to the command.

## Methods

### [`set_arguments(self, args: List[str], kwargs: Dict[str, Any])`](https://github.com/programminglaboratorys/nin0lib/blob/main/nin0lib/context.py#L14)

Sets the arguments and keyword arguments of the context.

### classmethod [`from_dict(cls, data: Dict[str, Any])`](https://github.com/programminglaboratorys/nin0lib/blob/main/nin0lib/context.py#L19)

Creates a new [Context](https://github.com/programminglaboratorys/nin0lib/blob/main/nin0lib/context.py#L8) object from a dictionary.

### [`create_context(cls, client: Client, message: Message)`](https://github.com/programminglaboratorys/nin0lib/blob/main/nin0lib/context.py#L26)

Creates a new [Context](https://github.com/programminglaboratorys/nin0lib/blob/main/nin0lib/context.py#L8) object from a client and a message.
s
