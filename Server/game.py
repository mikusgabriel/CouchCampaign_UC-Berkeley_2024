import asyncio
import json
import math
import time
import map

import numpy as np
import requests
from dotenv import dotenv_values
from openai import OpenAI

import meshyApi
from connections import Connections

config = dotenv_values(".env")

openAiClient = OpenAI(api_key=config["openAiKey"])


class Player:
    def __init__(
        self,
        userId: str,
        description: str,
        race: str,
        classe: str,
        meshyId: str,
        x: int,
        y: int,
    ) -> None:
        self._id = userId
        self._description = description
        self._race = race
        self._classe = classe
        self._meshyId = meshyId
        self._x = x
        self._y = y
        self.choices = None

    def id(self):
        return self._id

    def description(self):
        return self._description

    def race(self):
        return self._race

    def classe(self):
        return self._classe

    def meshy(self):
        return self._meshyId

    def position(self):
        return {"x": self._x, "y": self._y}

    def move(self, x: int, y: int):
        self._x = x
        self._y = y

    def setFullStatSheet(self, stats: dict[str, any]):
        self.level = stats["level"]
        self.alignment = stats["alignment"]
        self.background = stats["background"]
        self.experiencePoints = stats["experiencePoints"]
        self.attributes = stats["attributes"]
        self.skills = stats["skills"]
        self.savingThrows = stats["savingThrows"]
        self.armorClass = stats["armorClass"]
        self.hitPoints = stats["hitPoints"]
        self.hitDice = stats["hitDice"]
        self.speed = stats["speed"]
        self.proficiencies = stats["proficiencies"]
        self.equipment = stats["equipment"]
        self.features = stats["features"]
        self.spells = stats["spells"]
        self.personalityTraits = stats["personalityTraits"]
        self.ideals = stats["ideals"]
        self.bonds = stats["bonds"]
        self.flaws = stats["flaws"]
        self.notes = stats["notes"]
        self.currentConditions = stats["currentConditions"]

    def getFullStatSheet(self):
        return {
            "name": self._id,
            "classe": self._classe,
            "level": self.level,
            "race": self._race,
            "alignment": self.alignment,
            "background": self.background,
            "experiencePoints": self.experiencePoints,
            "attributes": self.attributes,
            "skills": self.skills,
            "savingThrows": self.savingThrows,
            "armorClass": self.armorClass,
            "hitPoints": self.hitPoints,
            "hitDice": self.hitDice,
            "speed": self.speed,
            "proficiencies": self.proficiencies,
            "equipment": self.equipment,
            "features": self.features,
            "spells": self.spells,
            "locations": {"x": self._x, "y": self._y},
            "personalityTraits": self.personalityTraits,
            "ideals": self.ideals,
            "bonds": self.bonds,
            "flaws": self.flaws,
            "notes": self.notes,
            "currentConditions": self.currentConditions,
        }

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
        self.whenDiceRoll = None
        self.setMap("base")

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
            for p in self._players.values():
                if p.choices is None:
                    await self._connections.send_client(
                        p.id(),
                        {
                            "type": "status",
                            "status": "lobby",
                            "data": {
                                "players": players,
                            },
                        },
                    )
                else:
                    await self._connections.send_client(
                        p.id(),
                        {
                            "type": "status",
                            "status": "choice",
                            "data": {
                                "choices": p.choices,
                            },
                        },
                    )

        else:
            for player in self._players.values():
                if player.choices is not None:
                    await self._connections.send_client(
                        player.id(),
                        {
                            "type": "status",
                            "status": "choice",
                            "data": {
                                "choices": player.choices,
                            },
                        },
                    )
                elif player == self.currentTurn["player"]:
                    if self.currentTurn.get("talkingTo", None) is not None:
                        await self._connections.send_client(
                            player.id(),
                            {
                                "type": "status",
                                "status": "talk",
                                "data": {"to": self.currentTurn["talkingTo"]},
                            },
                        )
                    else:
                        await self._connections.send_client(
                            player.id(),
                            {
                                "type": "status",
                                "status": "play",
                                "data": {"options": self.currentTurn["options"]},
                            },
                        )
                else:
                    await self._connections.send_client(
                        player.id(), {"type": "status", "status": "wait"}
                    )

    def setMap(self, mapId: str):
        for m in json.load(open("game_info/5e-SRD-Maps.json")):
            if m["mapid"] == mapId:
                self.currentMap = m
                break

        self.currentNpcs = []
        for npc in json.load(open("game_info/5e-SRD-Npcs.json")):
            if npc["name"] in self.currentMap["npcs"]:
                self.currentNpcs.append(npc)
                if len(self.currentNpcs) == len(self.currentMap["npcs"]):
                    break

        self.currentEnemies = []
        for enemy in json.load(open("game_info/5e-SRD-Enemies.json")):
            if enemy["name"] in self.currentMap["enemies"]:
                self.currentEnemies.append(enemy)
                if len(self.currentEnemies) == len(self.currentMap["enemies"]):
                    break

        for i, player in enumerate(self._players.values()):
            player.move(self.currentMap["spawningarea"][0][0][i])

    async def update_unity(self):
        imgBytes = map.image_to_string(self.currentMap["map"])
        await self._connections.send_unity(
            {
                "type": "map",
                "map": imgBytes,
                "entities": [
                    *[
                        {
                            "name": enemy["name"],
                            "meshyId": enemy["meshyid"],
                            **enemy["location"],
                        }
                        for enemy in self.currentEnemies
                    ],
                    *[
                        {
                            "name": npc["name"],
                            "meshyId": npc["meshyid"],
                            **npc["location"],
                        }
                        for npc in self.currentNpcs
                    ],
                    *[
                        {"name": player.id(), **player.position()}
                        for player in self._players.values()
                    ],
                ],
            }
        )

    async def startGame(self):
        player = list(self._players.values())[0]
        self.currentTurn = {"player": player, "playerIndex": 0}
        self.currentTurn["options"] = await self.getPlayerOptions(player)

    async def nextTurn(self):
        """Processes the end of the current player's turn"""

        playerIndex = self.currentTurn["playerIndex"] + 1
        if playerIndex >= len(self._players):
            playerIndex = 0
        player = list(self._players.values())[playerIndex]
        self.currentTurn = {"player": player, "playerIndex": playerIndex}
        self.currentTurn["options"] = await self.getPlayerOptions(player)

        # Notify
        await self.broadcast_client_info()
        await self._connections.send_unity({"type": "zoom", "name": player.id()})

    async def createPlayer(self, userId: str, race: str, classe: str, description: str):
        """Creates a player from the user's data"""

        [x, y] = self.currentMap["spawningarea"][0][len(self._players)]
        meshyId = meshyApi.generateMeshyMesh(race, classe, description)

        player = Player(
            userId, description, race, classe, meshyId, math.floor(x), math.floor(y)
        )
        self._players[userId] = player

        player.choices = self.getPlayerCreationChoices(classe, race)

        # Notify Unity
        await self._connections.send_unity(
            {
                "type": "spawn",
                "x": player.position()["x"],
                "y": player.position()["y"],
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

    def gameTurn(self, input):
        gptboolean = True
        game_history = json.load(open("./game_info/5e-SRD-DM-History.json"))["messages"]
        players = json.load(open("./game_info/5e-SRD-Players.json"))
        ennemies = json.load(open("./game_info/5e-SRD-Enemies.json"))

        game_history.append(
            {
                "role": "user",
                "content": input,
            }
        )
        counter = 1

        while gptboolean:
            response = openAiClient.chat.completions.create(
                model="gpt-4o",
                response_format={"type": "json_object"},
                messages=(
                    {
                        "role": "system",
                        "content": f"this is the game_history :{game_history}. You will be in control of the gameflow each turn. You will receive and input in this format: Player1 has used Fireball on you. You can use whatever function you want. You will have access to all the players: {players} and all the ennemies: {ennemies}. You will return the json of the person affected with the effects in use.",
                    },
                    {"role": "user", "content": "{input} make this work"},
                ),
                functions=[
                    {
                        "name": "getInfoDND",
                        "description": "This function allows you to search a key term and receive a json with all the info pertaining to the search term in DND. For example, if you search fireball, it will search for the spell fireball and give the stat sheet for fire ball. You",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "info_wanted": {
                                    "type": "string",
                                    "description": "Search term that will be the base for our search.",
                                }
                            },
                        },
                    },
                    {
                        "name": "DealDamage",
                        "description": "This function allows you to deal damage to an ennemy or a player. You will have to search the damage output first.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "damage": {
                                    "type": "int",
                                    "description": "The damage it will deal based on your research",
                                },
                                "name": {
                                    "type": "string",
                                    "description": "Name of the player so he can receive damage",
                                },
                            },
                        },
                    },
                    {
                        "name": "speakToPlayer",
                        "description": "This function will speak to the player. After you have either retrieved info, use this to tell the player the info. Do not ask anything after this. If the player has a question, then he can ask it himself.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "input": {
                                    "type": "string",
                                    "description": "What will be spoken to the player",
                                }
                            },
                        },
                    },
                ],
                function_call="auto",
            )
            answer = response.choices[0].message.function_call
            functionname = answer.name
            functionargs = json.loads(answer.arguments)
            if functionname == "getInfoDND":
                info = self.getInfoDND(functionargs["info_wanted"])
                game_history.append(
                    {
                        "role": "function",
                        "name": functionname,
                        "content": info,
                    }
                )
            elif functionname == "speakToPlayer":
                self._connections.send_unity(
                    {"type": "talk", "message": functionargs["input"]}
                )
                game_history.append(
                    {
                        "role": "function",
                        "name": functionname,
                        "content": info,
                    }
                )
                gptboolean = False

            elif functionname == "dealDamage":
                if self.getPlayer(functionargs["name"]):
                    (
                        self.getPlayer(functionargs["name"]).hitPoints
                        - functionargs["damage"]
                    )
                game_history.append(
                    {
                        "role": "function",
                        "name": functionname,
                        "content": info,
                    }
                )
            counter += 1
        f = open("./game_info/5e-SRD-DM-History.json", "w")
        json.dump(game_history, f, indent=6)

    # Make sure to look at the rules to know how many movements points and which abilities the current player can use. Each classe and race have their own unique passive and stats.
    async def getPlayerOptions(self, player: Player):
        self.currentTurn["messages"] = [
            {
                "role": "system",
                "content": """
You are the dungeon master of a game of dungeons and dragons. Make [no] assumptions about the game. I want you to call functions for searching.

Your role is to return a json object populated with the following keys, according to the current game state, once you have enough knowledge. Call the function to search for information about abilities, equipments, and spells.
- abilities: an array of objects containing name and description of every ability that the player can use this turn. Make sure to keep the description short and concise, so it can fit in one line. Only include spells that can be used by the player this turn. Do not include spells that the player canno't target and therefore cannot use.
- talk: an array of objects containing the x, the y, and the name corresponding to the position and name of thee NPCs who are close enough to the player for them to talk together. The player cannot talk to other players.
- fight: an array of objects containing the x, the y, and the name corresponding to the position and name of the enemies that are close enough to get attacked by the player this turn.

You can request any info you want about the game state, so do not hesistate to call the functions.
""",
            },
            {
                "role": "user",
                "content": f"""Player info: {player.getFullStatSheet()}.
                Map info: {json.dumps({'min': {'x': 0, 'y': 0}, 'max': {'x': 79, 'y': 39}})}
                Other players: {json.dumps([p.toPOJO() for p in self._players.values() if p != player])}
                NPCs: {self.currentEnemies}
                NPCs: {self.currentNpcs}""",
            },
        ]

        def gptGoesBrrrrr():
            response = openAiClient.chat.completions.create(
                model="gpt-4o",
                functions=[
                    {
                        "name": "getInfoDND",
                        "description": "This function allows you to search a key term and receive a json with all the info pertaining to the search term in DND. For example, if you search fireball, it will search for the spell fireball and give the stat sheet for fire ball.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "info_wanted": {
                                    "type": "string",
                                    "description": "Search term that will be the base for our search.",
                                }
                            },
                        },
                    }
                ],
                function_call="auto",
                response_format={"type": "json_object"},
                messages=self.currentTurn["messages"],
            )

            if response.choices[0].message.function_call is not None:
                answer = response.choices[0].message.function_call
                functionname = answer.name
                functionargs = json.loads(answer.arguments)

                if functionname == "getInfoDND":
                    info = self.getInfoDND(functionargs["info_wanted"])
                    self.currentTurn["messages"].append(
                        {
                            "role": "function",
                            "name": functionname,
                            "content": info,
                        }
                    )
                    return gptGoesBrrrrr()

            return json.loads(response.choices[0].message.content)

        res = gptGoesBrrrrr()
        res["move"] = self.coordinatesRange(
            30, (player.position()["x"], player.position()["y"])
        )
        res["allies"] = [
            {"name": p.id(), **p.position()}
            for p in self._players.values()
            if p != player
        ]
        res["npcs"] = [
            {"name": npc["name"], **npc["location"]} for npc in self.currentNpcs
        ]
        res["enemies"] = [
            {"name": enemy["name"], **enemy["location"]}
            for enemy in self.currentEnemies
        ]
        return res

    def coordinatesRange(self, speed: int, location: tuple[int, int]):
        range = math.floor(speed / 10)
        nparr = np.vstack(
            (
                np.tile(np.arange(-range, range + 1, 1), range * 2 + 1),
                np.floor(np.arange(0, (range * 2 + 1) ** 2, 1) / (range * 2 + 1))
                - range,
            )
        ).T + np.array(location)
        return nparr.tolist()

    async def rollDice(self, input: str):
        jsonFormat = {"type": "roll", "values": [4, 6, 6, 8, 10]}
        response = openAiClient.chat.completions.create(
            model="gpt-4o",
            response_format={"type": "json_object"},
            messages=[
                {
                    "role": "system",
                    "content": f"""Given the input, determine what must be rolled. Your output must in the json form of {jsonFormat}. 
                    Where for example if its 4d6 and 1d4 then the list [4,6,6,6,6].""",
                },
                {
                    "role": "user",
                    "content": f"Get the roll info for: {input}",
                },
            ],
        )

        await self._connections.send_unity(
            json.loads(response.choices[0].message.content)
        )

        def t(total: int):
            print(total)
            self.whenDiceRoll = None

        self.whenDiceRoll = t

    def getInfoDND(self, info_wanted: str):
        possible_endpoints = "ability-scores, alignments, backgrounds, classes, conditions, damage-types, equipment, equipment-categories, feats, features, languages, magic-items, magic-schools, monsters, proficiencies, races, rule-sections, rules, skills, spells, subclasses, subraces, traits, weapon-properties"
        payload = {}
        headers = {"Accept": "application/json"}

        jsonFormat = {"endpoint": "", "possible-terms-after-endpoint": []}
        response = openAiClient.chat.completions.create(
            model="gpt-4o",
            response_format={"type": "json_object"},
            messages=[
                {
                    "role": "system",
                    "content": f"""You are a search engine of a dnd db. You know these endpoints exist: {possible_endpoints}. 
                    The format is json: {jsonFormat}. You must choose an endpoint and 
                    then give three possible terms for after the end point for example. http://www.dnd5eapi.co/endpoint/term """,
                },
                {
                    "role": "user",
                    "content": f"I want the info about {info_wanted}",
                },
            ],
        )
        endpoints = json.loads(response.choices[0].message.content)

        for point in endpoints["possible-terms-after-endpoint"]:
            url = f"https://www.dnd5eapi.co/api/{endpoints['endpoint']}/{point}"

            response = requests.request("GET", url, headers=headers, data=payload)
            if response.text != '{"error":"Not found"}':
                return response.text

        return "No info found. You may invent."

    def talkToNPC(self, transcript: str, hume_analysis: list):
        for npc in self.currentNpcs:
            if npc["name"] == self.currentTurn["talkingTo"]:
                NPC_json = npc

        with open("game_info/5e-SRD-DM-History.json") as file:
            History_json = json.load(file)

        self.currentTurn["messages"].append(
            {
                "role": "user",
                "content": f"analysis:{hume_analysis}, Player_message: {transcript}",
            }
        )

        function = {
            "name": "stop_conversation",
            "description": "This function allows you to stop the conversation with the player if you feel like the emotion analysis is a threat to your life as a NPC. It could also be that you are annoyed by the players precense and you wish to be left alone. Everything is based on what the player says and their emotion analysis.",
            "parameters": {},
        }

        response = openAiClient.chat.completions.create(
            model="gpt-4o",
            functions=[function],
            messages=[
                {
                    "role": "system",
                    "content": f"""You are {NPC_json}. Realize that you are very important to the story. You are talking to {self.currentTurn["player"].getFullStatSheet()} and you will contribute to the existing story. The story is as follows: {History_json}. You also have the player emotion analysis to influence your responses, Example: ["happiness" : 0.08122], the more the analysis is closer to 1 the more the emotion is present. For example, if the player analysis results in an angry emotion, you will be colder to the player.""",
                },
                *self.currentTurn["messages"],
            ],
        )

        if "function_call" in response.choices[0].message:
            answer = response.choices[0].message.function_call
            functionname = answer.name

            if functionname == "stop_conversation":
                self.nextTurn()

        self.currentTurn["messages"].append(response.choices[0].message)
        return response.choices[0].message.content

    def getPlayerCreationChoices(self, class_chosen: str, race_chosen: str):
        jsonFormat = {
            "choices": [
                {
                    "name": " ",
                    "choice-count": 0,
                    "options": [{"name": "", "description": ""}],
                }
            ]
        }
        class_info = self.getInfoDND(class_chosen)
        race_info = self.getInfoDND(race_chosen)
        response = openAiClient.chat.completions.create(
            model="gpt-4o",
            response_format={"type": "json_object"},
            messages=[
                {
                    "role": "system",
                    "content": f"""You are a helpful assistant designed to give a json on what the player can choose as
                    options for the character. The format is json: {jsonFormat}. """,
                },
                {
                    "role": "user",
                    "content": f"The two jsons you must consider are {class_info} and {race_info}",
                },
            ],
        )

        res = response.choices[0].message.content
        return json.loads(res)["choices"]

    def createPlayerStatsSheet(
        self,
        class_chosen: str,
        race_chosen: str,
        choices: dict,
        name: str,
        description: str,
    ):
        stats = []

        while len(stats) < 6:
            stats.append(np.sum(np.sort(np.random.randint(1, 7, size=6))[-3:]))

        jsonFormat = json.load(open("game_info/5e-SRD-Character-Sheet.json"))
        class_info = self.getInfoDND(class_chosen)
        race_info = self.getInfoDND(race_chosen)
        response = openAiClient.chat.completions.create(
            model="gpt-4o",
            response_format={"type": "json_object"},
            messages=[
                {
                    "role": "system",
                    "content": f"""You are an assistant that will create the character sheet for a given character. 
                    The format is json: {jsonFormat}. """,
                },
                {
                    "role": "user",
                    "content": f"The two jsons you must consider are {class_info} and {race_info}. The player has chosen {choices}. The name is {name} and the description is {description}. The points you can attribute to the stats are {stats}. You must fill out the entire stat sheet like background, etc.",
                },
            ],
        )

        res = response.choices[0].message.content
        return json.loads(res)
