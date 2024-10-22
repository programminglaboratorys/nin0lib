from websockets.exceptions import ConnectionClosed, ConnectionClosedOK, ConnectionClosedError
from websockets.client import connect, WebSocketClientProtocol
from json import dumps as tojson, loads as fromjson
from commandkit.eventer import Eventer
from typing import AsyncIterable
from logging import getLogger

import asyncio
import logging

from .message import Message, User
from .opcodes import Opcodes, Packet

logger = getLogger(__name__)

class EventManager(Eventer):
	def _dispatch(self, event_name: str, /, *args, **kwargs):
		ev = "on_" + event_name
		try:
			coro = getattr(self, ev)
		except AttributeError:
			pass
		else:
			self.schedule_event(coro, ev, *args, **kwargs)

	def dispatch(self, event_name: str, /, *args, **kwargs):
		logger.debug("dispatch event %s", event_name)
		self._dispatch(event_name, *args, **kwargs)
		ev = "on_" + event_name
		for event in self.extra_events.get(ev, []):
			self.schedule_event(event, ev, *args, **kwargs)
    
	def schedule_event(self, event, ev,  /,*args,**kwargs):
		return asyncio.create_task(event(*args, **kwargs))

class Client(EventManager):
    username: str
    id: str
    socket: None|WebSocketClientProtocol
    token: None|str
    uri: str = "wss://chatws.nin0.dev/"
    _logger: logging.Logger = logger

    def __init__(self, *, token=None, **_) -> None:
        EventManager.__init__(self)
        self.socket = None
        self.token = token

    async def send(self, message):
        await self.raw_send(Packet(op=Opcodes.MESSAGE, d={"content": str(message)}).to_json())

    async def raw_send(self, packet: str):
        await self.socket.send(packet)

    async def receive(self) -> AsyncIterable[Packet]:
        async for message in self.socket:
            return Packet.from_json(message)
    
    async def _run(self):
        limit = 0
        while (limit := limit + 1) < 10:
            try:
                async with connect(self.uri) as websocket:
                    limit = 0
                    self.socket = websocket
                    self.dispatch("connect")
                    await self.raw_send(Packet(
                         op=Opcodes.LOGIN, 
                         d={"token": self.token, "device": "bot"}
                    ).to_json())
                    async for message in self.socket:
                        self.dispatch("raw_socket_message", message)
            except (ConnectionClosedOK, ConnectionClosed, KeyboardInterrupt) as e:
                self.dispatch("disconnect")
                logger.info(f"Connection closed: {e}")
                return
            except (ConnectionClosedError) as e:
                logger.info(f"Connection closed error {repr(e)}. Retrying...")
                await asyncio.sleep(1)
            except Exception as e:
                logger.info(f"An error happened {repr(e)}. Retrying...")
                self.dispatch("socket_exception", e)
                raise e
        logger.info("reached retry limit")
    
    def run(self, token: str, logger_level=logging.INFO):
        logger.setLevel(logger_level)
        self.token = token
        asyncio.run(self._run())
    
    def disconnect(self, reason: str=""):
        logger.debug("closing socket")
        self.socket.close(reason=reason)
    
    async def __aenter__(self):
        if self.socket is None:
            self.connect()
        return self
    
    def connect(self):
        """ Connect to the websocket server """
        async def inner():
            logger.debug("connecting to %s", self.uri)
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
            self.disconnect()
            self.socket = None
    
    def __enter__(self):
        if not asyncio.get_event_loop().is_running():
            raise RuntimeError("Client must be used with asyncio.run() or as an async context manager")
        return self
    
    def __exit__(self, *args):
        if not asyncio.get_event_loop().is_running():
            raise RuntimeError("Client must be used with asyncio.run() or as an async context manager")
        return self

    async def on_raw_login(self, raw):
        self.__dict__.update(raw)
        self.dispatch("ready")
    
    async def on_raw_heartbeat(self, raw):
        await self.raw_send(Packet(op=Opcodes.HEARTBEAT, d=raw).to_json())

    async def on_raw_socket_message(self, message: str):
        packet: Packet = Packet.from_json(message)
        match packet.op:
            case Opcodes.ERROR:
                  self.dispatch("socket_" + packet.op.name.lower(), packet.d)
            case Opcodes.MEMBER_LIST:
                self.dispatch(packet.op.name.lower(), map(User, packet.d["users"]))
            case Opcodes.MESSAGE:
                self.dispatch(packet.op.name.lower(), Message.from_dict(packet.d))
            case _:
                self.dispatch("raw_" + packet.op.name.lower(), packet.d)
