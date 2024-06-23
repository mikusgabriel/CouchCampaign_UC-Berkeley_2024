import requests
import base64
import re

pattern = re.compile(r'data-payload="([^"]*)"')
response = requests.get("https://ea41-104-196-242-9.ngrok-free.app/imagen").text




image_data = base64.b64decode(response)

with open("./maps/maptosave.png", "wb") as fh:
    fh.write(image_data)
print("Image saved successfully.")
