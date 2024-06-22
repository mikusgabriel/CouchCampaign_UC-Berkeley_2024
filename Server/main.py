import asyncio
import base64
import json

from fastapi import (
    Request,
    FastAPI,
    HTTPException,
    Response,
    WebSocket,
    WebSocketDisconnect,
)
from pydantic import BaseModel

import voiceApi
from connections import Connections
from game import GameManager

app = FastAPI()
connections = Connections()
gameManager = GameManager(connections)


class LoginBody(BaseModel):
    name: str


@app.post("/login")
async def login_POST(body: LoginBody, res: Response):
    userId = body.name
    res.set_cookie("id", userId)

    if gameManager.getPlayer(userId) is None:
        return {"success": True, "id": userId, "status": "create"}
    return {
        "success": True,
        "id": userId,
        "status": "wait",
        "user": gameManager.getPlayer(userId).toPOJO(),
    }


@app.post("/logout")
async def logout_POST(res: Response):
    res.delete_cookie("id")
    return {"success": True}


class PlayerCreateBody(BaseModel):
    race: str
    classe: str
    description: str


@app.post("/player/create")
async def player_create_POST(body: PlayerCreateBody, req: Request):
    userId = req.cookies.get("id")
    if userId is None:
        raise HTTPException(status_code=401, detail="Please login in first.")
    if gameManager.getPlayer(userId) is not None:
        raise HTTPException(status_code=400, detail="Player already exists.")

    if gameManager.currentTurn is not None:
        raise HTTPException(status_code=400, detail="A game is already in progress.")

    await gameManager.createPlayer(userId, body.race, body.classe, body.description)
    await connections.send_client(userId, {"type": "status", "status": "wait"})
    await connections.send_client(
        userId, {"type": "user", "user": gameManager.getPlayer(userId).toPOJO()}
    )
    return {"success": True}


@app.websocket("/player/ws")
async def ws_WEBSOCKET(ws: WebSocket):
    userId = ws.cookies.get("id")
    if userId is None:
        raise HTTPException(status_code=401, detail="Please login in first.")

    await ws.accept()
    connections.add_client(userId, ws)

    if gameManager.getPlayer(userId) is None:
        await connections.send_client(userId, {"type": "status", "status": "create"})
    else:
        await connections.send_client(userId, {"type": "status", "status": "wait"})
        await connections.send_client(
            userId, {"type": "user", "user": gameManager.getPlayer(userId).toPOJO()}
        )

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
