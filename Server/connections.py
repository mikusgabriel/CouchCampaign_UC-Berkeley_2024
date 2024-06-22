import asyncio

from fastapi import WebSocket


class Connections:
    def __init__(self) -> None:
        self._clients_ws: dict[str, WebSocket] = {}
        self._unity_ws = None

    def add_client(self, id: str, ws: WebSocket):
        self._clients_ws[id] = ws

    def remove_client(self, id: str):
        self._clients_ws.pop(id, None)

    def set_unity(self, ws: WebSocket):
        self._unity_ws = ws

    async def send_client(self, id: str, message):
        await self._clients_ws[id].send_json(message)

    async def broadcast_client(self, message):
        await asyncio.gather([self.send_client(id, message) for id in self._clients_ws])

    async def send_unity(self, message):
        if self._unity_ws:
            await self._unity_ws.send_json(message)
