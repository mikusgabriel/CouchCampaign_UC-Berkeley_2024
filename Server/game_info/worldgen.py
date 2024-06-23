import random
from PIL import Image
import numpy as np
import json
import random
from openai import OpenAI
import requests
import os 

def coordinatesRange(range,location):
    return np.vstack((np.tile(np.arange(-range,range+1,1),range*2+1),np.floor(np.arange(0,(range*2+1)**2,1) / (range*2+1)) - range)).T + location
    
def mapEnemyNpcPlacements(mapurl,npccount,enemycount):
    # Define color mappings
    PATHS = [
        (165, 42, 42),   # brown
        (210, 180, 140), # Path level 1
        (160, 82, 45),   # Path level 2
        (139, 69, 19),   # Path level 3
        (255, 140, 0),   # additional path color
    ]
    NOMOVEMENT = [
        (0, 0, 255)    # blue
    ]
    TILE_COLORS = {
        'grass': (0, 128, 0),    # green
        'path_level0': (165, 42, 42),   # brown
        'path_level1': (210, 180, 140), # Path level 1
        'path_level2': (160, 82, 45),   # Path level 2
        'path_level3': (139, 69, 19),   # Path level 3
        'water': (0, 0, 255),    # blue
        'forest': (0, 100, 0),   # dark green
        'sand': (255, 255, 0),   # yellow
        'rocklevel1': (128, 128, 128),
        'rocklevel2': (169, 169, 169),
        'rocklevel3': (211, 211, 211)
    }

    exitcolors = {
        0: np.array([255, 0, 0], dtype=np.uint8),
        1: np.array([0, 255, 0], dtype=np.uint8),
        2: np.array([0, 0, 255], dtype=np.uint8),
        3: np.array([255, 255, 0], dtype=np.uint8),
        4: np.array([255, 0, 255], dtype=np.uint8),
        5: np.array([0, 255, 255], dtype=np.uint8),
        6: np.array([255, 128, 128], dtype=np.uint8),
        7: np.array([128, 255, 128], dtype=np.uint8),
        8: np.array([128, 128, 255], dtype=np.uint8),
        9: np.array([255, 0, 128], dtype=np.uint8)
    }

    # Open the image and convert to numpy array
    image = Image.open(mapurl)
    a = np.array(image)
    blank = np.zeros((a.shape[0], a.shape[1]), dtype=np.int64)
    newimage = np.zeros(a.shape, dtype=np.uint8)

    # Process each pixel to classify
    for y in range(a.shape[0]):
        for x in range(a.shape[1]):
            pixel = tuple(a[y, x, :3])  # Ignore the alpha channel if present
            if pixel in PATHS:
                newimage[y, x, :3] = [255,255,255]

                blank[y, x] = 0
            elif pixel in NOMOVEMENT:
                blank[y, x] = 1
            else:
                blank[y, x] = 2

    adjacent = []
    spawnableareas = []
    safeadjacent = []

    # Process each pixel to find adjacent paths
    for y in range(blank.shape[0]):
        for x in range(blank.shape[1]):
            if x in [0, blank.shape[1]-1] or y in [0, blank.shape[0]-1]:
                if blank[y, x] == 0:
                    pixel = (y, x)
                    found = False
                    counter = 0
                    adjacenttiles = coordinatesRange(4,np.array([y,x]))
                    for list_index, pixel_list in enumerate(adjacent):
                        adjacenttiles = coordinatesRange(4,np.array([y,x]))
                        if any((pixel[0]-4 <= p[0] <= pixel[0]+4 and 
                                pixel[1]-4 <= p[1] <= pixel[1]+4) for p in pixel_list):
                            adjacent[list_index].append(pixel)
                            found = True
                            break
                        counter+=1

                    if not found:
                        adjacent.append([])
                        spawnableareas.append([])

                    color = exitcolors[len(adjacent) % 10]

                    
                    for adjacenttile in adjacenttiles:
                        if tuple(adjacenttile) not in spawnableareas[counter]:
                            if 40 > adjacenttile[0] >= 0 and 80 > adjacenttile[1] >= 0 :
                                spawnableareas[counter].append(tuple(adjacenttile))
                                newimage[int(adjacenttile[0]), int(adjacenttile[1]), :3] = color
                    
                    adjacenttiles = coordinatesRange(8,np.array([y,x]))

                    for adjacenttile in adjacenttiles:
                        if tuple(adjacenttile) not in safeadjacent:

                            safeadjacent.append(tuple(adjacenttile))



                    adjacent[counter].append(pixel)
                    color = exitcolors[len(adjacent) % 10]
                    newimage[y, x, :3] = color
    npcenemytiles = []
    # Process each pixel to find adjacent paths
    for y in range(blank.shape[0]):
        for x in range(blank.shape[1]):
            
                if blank[y, x] == 2:
                    pixel = (y, x)
                    if pixel not in npcenemytiles and pixel not in safeadjacent:
                        npcenemytiles.append(pixel)
                    
    enemytiles = []
    while len(enemytiles) < enemycount:
        index = random.randint(0,len(npcenemytiles)-1)
        
        newimage[npcenemytiles[index][0], npcenemytiles[index][1], :3] = [255,128,64]

        enemytiles.append(npcenemytiles[index])
        npcenemytiles.pop(index)
    npctiles = []
    while len(npctiles) < npccount:
        index = random.randint(0,len(npcenemytiles)-1)
        npctiles.append(npcenemytiles[index])
        newimage[npcenemytiles[index][0], npcenemytiles[index][1], :3] = [64,128,255]
        npcenemytiles.pop(index)

    print(adjacent)
    print(f"Number of adjacency groups: {len(adjacent)}")
    im = Image.fromarray(newimage)
    im.save('test.png')
    print("Image processing complete.")
    return enemytiles, npctiles, spawnableareas


functions = [
   {
      "name": "getInfoDND",
      "description": "This function allows you to search a key term and receive a json with all the info pertaining to the search term in DND. For example, if you search fireball, it will search for the spell fireball and give the stat sheet for fire ball.",
      "parameters": {
         "type": "object",
         "properties": {
            "info_wanted": {
               "type": "string",
               "description": "Search term that will be the base for our search."
            }
         }
      }
   }
]
def getMeshID(promptInput):

    payload = {
        "mode": "preview",
        "prompt": f"{promptInput}",
        "art_style": "realistic",
        "negative_prompt": "low quality, low resolution, low poly, ugly, has a base, has no feet, not dnd style",
    }
    apiKey = "msy_fIpmhBKgcBzOef383zGyxNIpFjUPdOWtAH5O"
    headers = {"Authorization": f"Bearer {apiKey}"}

    response = requests.post(
        "https://api.meshy.ai/v2/text-to-3d",
        headers=headers,
        json=payload,
    )
    response.raise_for_status()
    print(response.json())
    return response.json()["result"]

def getInfoDND(info_wanted: str):
    
    possible_endpoints = "ability-scores, alignments, backgrounds, classes, conditions, damage-types, equipment, equipment-categories, feats, features, languages, magic-items, magic-schools, monsters, proficiencies, races, rule-sections, rules, skills, spells, subclasses, subraces, traits, weapon-properties"
    payload = {}
    headers = {
      'Accept': 'application/json'
    }

    jsonFormat = {
        "endpoint": "",
        "possible-terms-after-endpoint": []
    }
    response = client.chat.completions.create(
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

    return "no info found. You may invent"

class mapNode():
    def __init__(self, maptype, biome):
        self.name = ""
        self.biome = biome
        self.maptype = maptype
        self.description = ""
        self.npcs = []
        self.enemies = []
        self.connectingnodes = []
        self.imageurl = ""
        self.enemytiles = []
        self.npctiles = []
        self.entrancenumbers = []
        self.entrancelocations = []
        self.entracenumbers = []
        
client = OpenAI(api_key="sk-proj-xklwW5mYFK3AmpTgxULaT3BlbkFJP1pz572EVZqPRXxcNIy6")
places = [
    "Random Encounter",
    # "Town",
    # "Dungeon",
    "Wilderness",
    # "Ruins"
]
biomes = [
    "river",
    "Forest",
    "Lake",
    "Mountain",  
    "Mountain Side",    
]
def generateNodeName(biome_chosen, type_chosen):
    jsonFormat = {
        "name": "",
    }
    response = client.chat.completions.create(
        model="gpt-4o",
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": f"You are to choose an original name for the following area type and biome given. "
                           f"I will give you the type. The JSON format is the following {jsonFormat}",
            },
            {
                "role": "user",
                "content": f"Create a {type_chosen} in the {biome_chosen} type.",
            },
        ],
    )

    name = json.loads(response.choices[0].message.content)["name"]

    return name
def generateDescription(biome_chosen, type_chosen, name,connecting_nodes):
    jsonFormat = {
        "description": "",
        "npcs": [],
        "enemies": []
    }
    response = client.chat.completions.create(
        model="gpt-4o",
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": f"You are to choose an original description for the following area type and biome given and name and connecting areas. You will also decide the npcs and enemies in that location, Upto 2, and just the names of them no extra description. The enemies can be like Wood woad, wood woad, wood woad, owlbear. Try to use dnd enemies for random encours like owlbear, wood woad, etc."
                           f"I will give you the type. The JSON format is the following {jsonFormat}. If its a random encounter. use classic dnd enemies. If there are no npcs or enemies, you must leave the list empty. Please make the enemies coherant, you can even add multiple enemies together."},
            {
                "role": "user",
                "content": f"Description for {type_chosen} in the {biome_chosen} type called {name} knowing its connected to the following areas: {connecting_nodes}",
            },
        ],
    )
    description, npcs, enemies = json.loads(response.choices[0].message.content)["description"], json.loads(response.choices[0].message.content)["npcs"], json.loads(response.choices[0].message.content)["enemies"]
    return description, npcs, enemies

def generateWorld():
    totalentrances = []
    npclist = []
    enemylist = []
    map_connection_dict = {}
    map_node_list = []
    currentnodecount = 0

    images = os.listdir("./maps")

    # Initialize the first node
    first_biome = random.choice(biomes)
    first_type = random.choice(places)
    first_name = generateNodeName(first_biome, first_type)
    first_node = mapNode(first_type, first_biome)
    first_node.name = first_name
    index = random.randint(0,len(images)-1)
    first_node.mapurl = "./maps/" + images[index]
    # images.pop(index)

    map_node_list.append(first_node)

    first_node.description, first_node.npcs, first_node.enemies = generateDescription(first_node.biome, first_node.maptype, first_node.name, first_node.connectingnodes)
    first_node.enemytiles, first_node.npctiles, first_node.entrancelocations = mapEnemyNpcPlacements(first_node.mapurl,len(first_node.npcs),len(first_node.enemies))
    counter = 0
    for names in first_node.npcs:
        npclist.append(generateNPC(f"Name: {names}. Area they are in: {first_node.description} and located at {first_node.npctiles[counter]}"))
        counter +=1
    counter = 0
    for names in first_node.enemies:
        print(counter)
        enemylist.append(generateNPC(f"Name: {names}. Area they are in: {first_node.description} and located at {first_node.enemytiles[counter]}"))
        counter+=1

    prevnodecount = 0
    currentnodecount = len(first_node.entrancelocations)
    first_node.entrancenumbers = [x + prevnodecount for x in range(1, currentnodecount + 1)]
    print(first_node.entrancenumbers)

    completemap = []
    # Output or further processing
    for node in map_node_list:
        completemap.append({
            "name": node.name,
            "type": node.maptype,
            "biome": node.biome,
            "description": node.description,
            "connections": [n.name for n in node.connectingnodes],
            "npcs": node.npcs,
            "enemies": node.enemies,
            "map": node.mapurl,
            "entrancenumbers": first_node.entrancenumbers,
            "entrancecount": len(node.entrancelocations),
            "spawningarea": node.entrancelocations
        })

    f = open("5e-SRD-Maps.json", "w")
    json.dump(completemap,f,indent=5)
    f.close()


    f = open("5e-SRD-Npcs.json", "w")
    json.dump(npclist,f,indent=5)
    f.close()
    f = open("5e-SRD-Enemies.json", "w")
    json.dump(enemylist,f,indent=5)
    f.close()    

def generateNPC(prompt):
    jsonFormat = json.load(open("5e-SRD-NPC-Sheet.json"))

    messages=[
        {
            "role": "system",
            "content": f"You are to create a dnd enemy or npc given the prompt. If it is an enemy, you must call call the getInfo function to get the necessary info before. You may choose the stats to be balanced. "
                        f"I will give you the type. The JSON format is the following {jsonFormat}"
                                    },
        {
            "role": "user",
            "content": prompt,
        },
    
    ]
    gptResponse = True
    while gptResponse:
        response = client.chat.completions.create(
            model="gpt-4o",
            response_format={"type": "json_object"},
            messages=messages,
            functions=functions,
        )
        answer = response.choices[0].message.content
        if answer is not None:

            gptResponse = False

            
            result = (answer)

        else: 
            answer = response.choices[0].message.function_call

            functionname = answer.name
            functionargs = json.loads(answer.arguments)
            if functionname == "getInfoDND":
                info = getInfoDND(functionargs["info_wanted"])
                messages.append({
                            "role": "function",
                            "name": functionname, 
                            "content": info,
                        })
                
    result = json.loads(result)
    result["meshyid"] = None
    # result["meshyid"] = getMeshID(result["appearance"])

    return result
                
    
generateWorld()