from dotenv import dotenv_values
from hume import HumeBatchClient
from hume.models.config import ProsodyConfig
from openai import OpenAI

config = dotenv_values(".env")

humeClient = HumeBatchClient(config["humeKey"])
openAiClient = OpenAI(api_key=config["openAiKey"])


async def getVoiceEmotions(file: bytes):
    with open("humeVoiceFile.webm", mode="wb") as file:
        file.write(file)

    config = ProsodyConfig()
    job = humeClient.submit_job(None, [config], files=["humeVoiceFile.webm"])
    job.await_complete()

    try:
        emotionsresults = job.get_predictions()[0]["results"]["predictions"][0][
            "models"
        ]["prosody"]["grouped_predictions"][0]["predictions"][0]["emotions"]

        first = 0
        firstemotion = ""
        second = 0
        secondemotion = ""
        third = 0
        thirdemotion = ""
        for emotions in emotionsresults:
            if emotions["score"] > first:
                first = emotions["score"]
                firstemotion = emotions
            elif emotions["score"] > second:
                second = emotions["score"]
                secondemotion = emotions
            elif emotions["score"] > third:
                third = emotions["score"]
                thirdemotion = emotions

        return [firstemotion, secondemotion, thirdemotion]
    except Exception as e:
        print("Hume error:", e)
        return []


async def getVoiceTranscript(file: bytes):
    transcription = openAiClient.audio.transcriptions.create(
        model="whisper-1", file=file, response_format="text"
    )
    return transcription
