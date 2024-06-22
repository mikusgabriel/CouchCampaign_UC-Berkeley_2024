import asyncio
import base64
import json

from fastapi import FastAPI, Response, WebSocket, WebSocketDisconnect
from pydantic import BaseModel

import voiceApi
from connections import Connections
from game import GameManager

app = FastAPI()
connections = Connections()
gameManager = GameManager()


class LoginInfo(BaseModel):
    name: str


@app.post("/login")
async def login_POST(info: LoginInfo, res: Response):
    userId = info.name
    res.set_cookie("id", userId)

    if gameManager.getPlayer(userId) is None:
        return {"success": True, "id": userId, "state": "create"}
    return {
        "success": True,
        "id": userId,
        "state": "wait",
        "user": gameManager.getPlayer(userId).toPOJO(),
    }


@app.post("/logout")
async def logout_POST(res: Response):
    res.delete_cookie("id")
    return {"success": True}


@app.websocket("/ws")
async def ws_WEBSOCKET(ws: WebSocket):
    userId = ws.cookies.get("id")
    if (userId is None) or (gameManager.getPlayer(userId) is None):
        return {"success": False, "message": "Please login in first."}

    await ws.accept()
    connections.add_client(userId, ws)

    if gameManager.getPlayer(userId) is None:
        await connections.send_client(userId, {"type": "user", "state": "create"})

    try:
        while True:
            data = json.loads(await ws.receive_text())
            print("User data:", userId, data)

            match data["type"]:
                case "end-turn":
                    if gameManager.currentTurn.player.id() != userId:
                        continue
                    await gameManager.nextTurn()

                case "voice":
                    if gameManager.currentTurn.player.id() != userId:
                        continue

                    encodedAudioData = data["recording"].split(",")[1]
                    audioData = base64.b64decode(encodedAudioData)
                    [transcript, emotions] = await asyncio.gather(
                        voiceApi.getVoiceTranscript(audioData),
                        voiceApi.getVoiceEmotions(audioData),
                    )

                    await ws.send_json({"type": "transcript", "data": transcript})

                case "create":
                    if gameManager.currentTurn is not None:
                        await ws.send_json(
                            {
                                "type": "error",
                                "message": "A game is already in progress",
                            }
                        )
                        continue

                    await gameManager.createPlayer(
                        userId, data["race"], data["classe"], data["description"]
                    )

                case "move":
                    if gameManager.currentTurn.player.id() != userId:
                        continue

                    await gameManager.movePlayer(userId, data["x"], data["y"])
                    await gameManager.nextTurn()

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
            print("Unity WebSocket received:", data)

    except WebSocketDisconnect:
        connections.set_unity(None)
