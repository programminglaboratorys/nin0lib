# Opcodes

The [Opcodes](https://github.com/programminglaboratorys/nin0lib/blob/main/nin0lib/opcodes.py#L5) int enum represents different opcodes that can be used in a packet.

## Enum Values

### `MESSAGE`

The `MESSAGE` opcode represents a message packet.

### `LOGIN`

The `LOGIN` opcode represents a login packet.

### `HEARTBEAT`

The `HEARTBEAT` opcode represents a heartbeat packet.

### `MESSAGE_HISTORY`

The `MESSAGE_HISTORY` opcode represents a message history packet.

### `ERROR`

The `ERROR` opcode represents an error packet.

## Packet

The [Packet](https://github.com/programminglaboratorys/nin0lib/blob/main/nin0lib/opcodes.py#L13) is a dataclass; class represents a packet that can be sent over the network.

## Fields

### `op`: [Opcodes](https://github.com/programminglaboratorys/nin0lib/blob/main/nin0lib/opcodes.py#L5)

The opcode of the packet.

### `d`: `Dict[str, Any]`

The data of the packet.

## Methods

### `to_json(self)`

Returns a JSON representation of the packet.

### `from_json(cls, string: str)`

Creates a new [Packet](https://github.com/programminglaboratorys/nin0lib/blob/main/nin0lib/opcodes.py#L13) object from a JSON string.

## Example

```python
packet = Packet(
    op=Opcodes.MESSAGE,
    d={"content": "Hello, world!"}
)
print(packet.to_json())
```
