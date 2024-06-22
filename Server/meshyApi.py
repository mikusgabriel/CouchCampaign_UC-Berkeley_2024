import requests
from dotenv import dotenv_values

config = dotenv_values(".env")


def generateMeshyMesh(race: str, classe: str, decription: str):
    response = requests.post(
        "https://api.meshy.ai/v2/text-to-3d",
        headers={"Authorization": f"Bearer {config['meshyKey']}"},
        json={
            "mode": "preview",
            "prompt": f"A {classe} {race} character in a dnd game. {decription}",
            "art_style": "realistic",
            "negative_prompt": "low quality, low resolution, low poly, ugly, has a base, has no feet",
        },
    )

    try:
        response.raise_for_status()
        print(response.json())
        return response.json()["result"]
    except Exception as e:
        print("Meshy error", e)
        return "invalid-meshy-id"
