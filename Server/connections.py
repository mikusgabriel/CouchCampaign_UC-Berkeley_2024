import asyncio

from fastapi import WebSocket


class Connections:
    def __init__(self) -> None:
        self._clients_ws: dict[str, WebSocket] = {}
        self._unity_ws = None

    def add_client(self, id: str, ws: WebSocket):
        self._clients_ws[id] = ws
        print("Websocket connected:", id)

    def remove_client(self, id: str):
        self._clients_ws.pop(id, None)
        print("Websocket disconnected:", id)

    def set_unity(self, ws: WebSocket):
        self._unity_ws = ws

        if ws is None:
            print("Unity disconnected")
        else:
            print("Unity connected")

    async def send_client(self, id: str, message):
        await self._clients_ws[id].send_json(message)

    async def broadcast_client(self, message):
        await asyncio.gather([self.send_client(id, message) for id in self._clients_ws])

    async def send_unity(self, message):
        if self._unity_ws:
            await self._unity_ws.send_json(message)
