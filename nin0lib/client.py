from json import dumps as tojson, loads as fromjson
from typing import AsyncIterable
from websockets.client import connect, WebSocketClientProtocol
import websockets

import asyncio

from .message import Message

class Client:
    username: str
    socket: None|WebSocketClientProtocol
    key: None|str
    uri: str = "wss://guhws.nin0.dev/"
    def __init__(self, *, username, key=None) -> None:
        self.username = username
        self.socket = None
        self.key = key

    async def send(self, message):
        await self.socket.send(tojson({
            "username": self.username,
            "content": message,
            "key": self.key,
        }))

    async def receive(self) -> AsyncIterable[str]:
        async for message in self.socket:
            return fromjson(message)
    
    async def _run(self):
        limit = 0
        while (limit := limit + 1) < 10:
            try:
                async with connect(self.uri) as websocket:
                    limit = 0
                    self.socket = websocket
                    async for message in self.socket:
                        data: dict = fromjson(message)
                        if data.get("op") != None:
                            for message in data["messages"]:
                                message: dict
                                message["username"] = message.pop("user")
                            await self.on_previous_messages(data["op"], list(map(lambda m: Message(**m), data["messages"])))
                            continue
                        await self.on_message(Message(**data))
            except (websockets.exceptions.ConnectionClosedError) as e:
                print(f"Connection closed {e}. Retrying...")
                await asyncio.sleep(1)
            except Exception as e:
                print(f"An error happened {e}. Retrying...")
                await asyncio.sleep(1)
        print("reached retry limit")
    
    def run(self, key: str):
        self.key = key
        asyncio.run(self._run())
    
    async def __aenter__(self):
        if self.socket is None:
            self.connect()
        return self
    
    def connect(self):
        async def inner():
            self.socket = await connect(self.uri)
        loop = asyncio.get_event_loop()
        if loop.is_running(): 
            task = loop.create_task(inner())
            loop.run_until_complete(task) 
        else:
            loop = asyncio.new_event_loop()
            loop.run_until_complete(inner())
            loop.close()

    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.socket is not None:
            await self.socket.close()
            self.socket = None
    
    def __enter__(self):
        if not asyncio.get_event_loop().is_running():
            raise RuntimeError("Client must be used with asyncio.run() or as an async context manager")
        return self
    
    def __exit__(self, *args):
        raise RuntimeError("Client must be used with asyncio.run() or as an async context manager")

    async def on_message(self, message: Message):
        pass
    
    async def on_previous_messages(self, op: int, messages: list[Message]):
        pass