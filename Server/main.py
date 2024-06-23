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
    return {
        "success": True,
        "id": userId,
    }


@app.post("/logout")
async def logout_POST(res: Response):
    res.delete_cookie("id")
    return {"success": True}


@app.post("/player/start")
async def player_start_POST(req: Request):
    userId = req.cookies.get("id")
    if userId is None:
        raise HTTPException(status_code=401, detail="Please login in first.")
    if gameManager.getPlayer(userId) is None:
        raise HTTPException(status_code=400, detail="Player doesn't exists.")

    if gameManager.currentTurn is not None:
        raise HTTPException(status_code=400, detail="The game is already in progress.")

    await gameManager.startGame()
    await gameManager.broadcast_client_info()
    return {"success": True}


class PlayerPlayBody(BaseModel):
    action: str
    x: int
    y: int
    # name: str | None = None


@app.post("/player/play")
async def player_play_POST(body: PlayerPlayBody, req: Request):
    userId = req.cookies.get("id")
    if userId is None:
        raise HTTPException(status_code=401, detail="Please login in first.")
    if gameManager.getPlayer(userId) is None:
        raise HTTPException(status_code=400, detail="Player doesn't exists.")

    if gameManager.currentTurn is None:
        raise HTTPException(status_code=400, detail="The game hasn't started yet.")

    match body.action:
        case "move":
            await gameManager.movePlayer(userId, body.x, body.y)
            await gameManager.nextTurn()

        case "talk":
            # await gameManager.movePlayer(userId, body.x, body.y)
            pass

        case "fight":
            # await gameManager.movePlayer(userId, body.x, body.y)
            pass

    await gameManager.broadcast_client_info()
    return {"success": True}


class PlayerDeleteBody(BaseModel):
    name: str


@app.post("/player/kick")
async def player_kick_POST(body: PlayerDeleteBody, req: Request):
    userId = req.cookies.get("id")
    if userId is None:
        raise HTTPException(status_code=401, detail="Please login in first.")
    if gameManager.getPlayer(userId) is None:
        raise HTTPException(status_code=400, detail="Player doesn't exists.")

    if gameManager.currentTurn is not None:
        raise HTTPException(status_code=400, detail="The game is already in progress.")

    gameManager.removePlayer(body.name)
    await connections.send_client(body.name, {"type": "status", "status": "create"})
    await gameManager.broadcast_client_info()
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
        raise HTTPException(status_code=400, detail="The game is already in progress.")

    await gameManager.createPlayer(userId, body.race, body.classe, body.description)
    await gameManager.broadcast_client_info()
    return {"success": True}


class PlayerChoiceBody(BaseModel):
    selected: list[str]


@app.post("/player/choice")
async def player_choice_POST(body: PlayerChoiceBody, req: Request):
    userId = req.cookies.get("id")
    if userId is None:
        raise HTTPException(status_code=401, detail="Please login in first.")
    if gameManager.getPlayer(userId) is None:
        raise HTTPException(status_code=400, detail="Player doesn't exists.")

    if gameManager.currentTurn is None:
        raise HTTPException(status_code=400, detail="The game hasn't started yet.")

    # await gameManager.createPlayer(userId, body.race, body.classe, body.description)
    await connections.send_client(userId, {"type": "status", "status": "wait"})
    return {"success": True}


@app.websocket("/player/ws")
async def ws_WEBSOCKET(ws: WebSocket):
    userId = ws.cookies.get("id")
    if userId is None:
        raise HTTPException(status_code=401, detail="Please login in first.")

    await ws.accept()
    connections.add_client(userId, ws)

    if gameManager.getPlayer(userId) is None:
        await ws.send_json({"type": "status", "status": "create"})
    else:
        await gameManager.broadcast_client_info()

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
