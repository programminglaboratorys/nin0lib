# Client

The [`Client`](https://github.com/programminglaboratorys/nin0lib/blob/main/nin0lib/client.py#L36) class represents a client that can connect to a chat server.

## Inheritance

The `Client` class inherits from `EventManager`.

## Fields

### `username`: `str`

The username of the client.

### `id`: `str`

The ID of the client.

### socket: `WebSocketClientProtocol | None`

The WebSocket client protocol of the client.

### `token`: `str | None`

The token of the client.

### `uri`: `str`

The URI of the chat websocket server.

## Methods

### `__init__(self, *, token: str = None)`

Initializes the client object.

### `event(func)`

The `event` decorator is used to register a function as an event in the class. for available events check [here](https://github.com/programminglaboratorys/nin0lib/blob/main/nin0lib.docs/events.md)

### `add_listen(func: Callable, name: str=None)`

Registers a function as an event in the class. The event is triggered when the event is dispatched.
if the name is None, it will be set to the function name

### `remove_listen(self, func: Callable, name: str=None)`

Removes a function from the event list.
if the name is None, it will use the function name to search for the event list

### `connect(self)`

Connects the client to the chat server.

### `disconnect(self, reason: str = "")`

Disconnects the client from the chat server.

### `send(self, message: str)`

Sends a message to the chat server.

### `raw_send(self, packet: str)`

Sends a raw packet to the chat server.

### `receive(self)`

Receives a packet from the chat server.

### `run(self, token: str, logger_level: int = logging.INFO)`

Runs the client main loop.

### `__enter__(self)`

Enters the client context.

> [!NOTE]
> This method raises a `RuntimeError`, as the client must be used with `asyncio.run()` or as an async context manager.

### `__exit__(self, exc_type, exc_val, exc_tb)`

Exits the client context.

> [!NOTE]
> This method raises a `RuntimeError`, as the client must be used with `asyncio.run()` or as an async context manager.

### `__aenter__(self)`

Asynchronously enters the client context.

### `__aexit__(self, exc_type, exc_val, exc_tb)`

Asynchronously exits the client context. and closes the socket on exit

## Example

```python
async def main():
    async with Client(token="my_token") as client:
        await client.send("Hello, world!")

asyncio.run(main())
```

> [!WARNING]
> those aren't all the class methods, you can check the code for more information or methods
