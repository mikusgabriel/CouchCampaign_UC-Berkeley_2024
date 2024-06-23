import asyncio

import meshyApi
from connections import Connections


class Player:
    def __init__(
        self, userId: str, race: str, classe: str, meshyId: str, x: int, y: int
    ) -> None:
        self._id = userId
        self._race = race
        self._classe = classe
        self._meshyId = meshyId
        self._x = x
        self._y = y

    def id(self):
        return self._id

    def position(self):
        return [self._x, self._y]

    def move(self, x: int, y: int):
        self._x = x
        self._y = y

    def toPOJO(self):
        return {
            "name": self._id,
            "race": self._race,
            "classe": self._classe,
            "meshyId": self._meshyId,
            "x": self._x,
            "y": self._y,
        }


class GameManager:
    def __init__(self, connections: Connections) -> None:
        self._players: dict[str, Player] = {}
        self._connections = connections
        self.currentTurn = None

    async def broadcast_client_info(self):
        await asyncio.gather(
            *[
                self._connections.send_client(
                    p.id(), {"type": "user", "user": p.toPOJO()}
                )
                for p in self._players.values()
            ]
        )

        if self.currentTurn is None:
            players = [p.toPOJO() for p in self._players.values()]
            await asyncio.gather(
                *[
                    self._connections.send_client(
                        p.id(),
                        {
                            "type": "status",
                            "status": "lobby",
                            "data": {
                                "players": players,
                            },
                        },
                    )
                    for p in self._players.values()
                ]
            )
        else:
            for player in self._players.values():
                if player == self.currentTurn.player:
                    self._connections.send_client(
                        player.id(), {"type": "status", "status": "play"}
                    )
                else:
                    self._connections.send_client(
                        player.id(), {"type": "status", "status": "wait"}
                    )

    async def nextTurn(self):
        """Processes the end of the current player's turn"""

        # Notify client
        await self._connections.send_client(
            self.currentTurn.player.id(), {"type": "state", "state": "wait"}
        )

        # Next turn
        playerIndex = self.currentTurn.playerIndex + 1
        if playerIndex >= len(self._players):
            playerIndex = 0
        player = self._players.values()[playerIndex]
        self.currentTurn = {"player": player, "playerIndex": playerIndex}

        # Notify client
        await self._connections.send_client(
            self.currentTurn.player.id(), {"type": "state", "state": "play"}
        )

        # Notify Unity
        await self._connections.send_unity(
            {"type": "current_player", "player": player.toPOJO()}
        )

    async def createPlayer(self, userId: str, race: str, classe: str, description: str):
        """Creates a player from the user's data"""

        [x, y] = [0, 0]
        # meshyId = meshyApi.generateMeshyMesh(race, classe, description)

        player = Player(userId, race, classe, "meshyId", x, y)
        self._players[userId] = player

        # Notify client
        await self._connections.send_client(
            userId, {"type": "user", "user": player.toPOJO()}
        )
        await self._connections.send_client(
            userId, {"type": "status", "status": "wait"}
        )

        # Notify Unity
        await self._connections.send_unity(
            {
                "type": "spawn",
                "x": player.position()[0],
                "y": player.position()[1],
                "name": userId,
                "meshyId": player.toPOJO()["meshyId"],
            }
        )
        return player

    def removePlayer(self, userId: str):
        return self._players.pop(userId, None)

    def getPlayer(self, userId: str):
        """Returns the specified player, or None"""

        return self._players.get(userId, None)

    async def movePlayer(self, userId: str, x: int, y: int):
        """Moves a player"""

        self.getPlayer(userId).move(x, y)

        # Notify Unity
        await self._connections.send_unity(
            {
                "type": "move",
                "name": userId,
                "positions": [
                    {"x": x, "y": x},
                ],
            }
        )
