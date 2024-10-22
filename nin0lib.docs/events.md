### `on_socket_error`

Triggered when an error is received from the socket.

### `on_message(message: Message)`

Triggered when a chat message is received.

### `on_member_list(users: Iterator[User])`

Triggered when a member list is received or updated.

### `on_raw_socket_message(message: str)`

Triggered when a raw message is received from the socket.

`on_raw_message` and `on_raw_socket_message` are not related, one receives a raw message from chat and the other receives a raw socket message.

## `on_raw_{opcode}`

Triggered when a raw packet with the specified opcode is received.

These events are dispatched by the `on_raw_socket_message` method, which handles incoming packets from the socket. The `on_socket_error` and `on_message` events are dispatched based on the opcode of the packet, while the `on_raw_{opcode}` events are dispatched for any other opcodes.

### `on_raw_login(raw: dict)`

Triggered when a raw login is received.

### `on_raw_heartbeat(raw: dict)`

Triggered when a raw heartbeat is received.

### `on_raw_message_history(raw: dict)`

Triggered when a raw message history is received.

### `on_raw_message(raw: dict)`

Triggered when a raw message is received.

Note that these events are dispatched based on the opcode of the packet, and the `on_raw_{opcode}` events are dispatched for any other opcodes.

> [!NOTE]
> to know the structure of those raw events, please refer to nin0 offical [Gateway documentation](https://github.com/nin0chat/docs/wiki/Gateway)
