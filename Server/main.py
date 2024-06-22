import asyncio
import base64
import json

from fastapi import FastAPI, Response, WebSocket, WebSocketDisconnect
from pydantic import BaseModel

import voiceApi
import meshyApi
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

            recordingAudioData = base64.b64decode(data["recording"].split(",")[1])
            [transcript, emotions] = asyncio.gather(
                voiceApi.getVoiceTranscript(recordingAudioData),
                voiceApi.getVoiceEmotions(recordingAudioData),
            )

            connections.send_client(userId, {"type": "transcript", "data": transcript})

    except WebSocketDisconnect:
        connections.remove_client(userId)
        print("websocket disconnected")


@app.websocket("/ws/unity")
async def ws_WEBSOCKET_UNITY(ws: WebSocket):
    await ws.accept()
    connections.set_unity(ws)

    try:
        while True:
            data = json.dumps(await ws.receive_text())
            print("received", data)

    except WebSocketDisconnect:
        connections.set_unity(None)
        print("websocket disconnected")
