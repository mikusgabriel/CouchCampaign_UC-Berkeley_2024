import json

from fastapi import FastAPI, Response, WebSocket, WebSocketDisconnect
from pydantic import BaseModel

from connections import Connections

app = FastAPI()
connections = Connections()


class LoginInfo(BaseModel):
    name: str


@app.post("/login")
async def login_POST(info: LoginInfo, res: Response):
    userId = info.name
    res.set_cookie("id", userId)

    return {"success": True, "id": userId}


@app.post("/logout")
async def logout_POST(res: Response):
    res.delete_cookie("id")
    return {"success": True}


@app.websocket("/ws")
async def ws_WEBSOCKET(ws: WebSocket):
    userId = ws.cookies.get("id")
    if userId is None:
        return {"success": False, "message": "Missing user id. Please login in first."}

    await ws.accept()
    connections.add_client(userId, ws)

    try:
        while True:
            data = json.loads(await ws.receive_text())
            print("User data:", userId, data)

    except WebSocketDisconnect:
        connections.remove_client(userId)
        print("websocket disconnected")
