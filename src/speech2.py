from xml.etree import ElementTree
import os
from azure.cognitiveservices import speech
import requests
import asyncio
from shutterstock_utils import get_video
from text_analysis import get_important
from speech_key import speech_key

from src.speech import QQQ

service_region = "eastus2"

speechconfig = speech.SpeechConfig(subscription=speech_key, region=service_region)
speech_recognizer = speech.SpeechRecognizer(speech_config=speechconfig)


def get_token():
    fetch_token_url = "https://eastus2.api.cognitive.microsoft.com/sts/v1.0/issueToken"
    headers = {
        'Ocp-Apim-Subscription-Key': speech_key
    }
    response = requests.post(fetch_token_url, headers=headers)
    return str(response.text)


class SpeechRecognizer:
    url = "https://billwurtz.com/snail-time.mp4"
    speech_thing = ""
    total=""
    async def get_video(self):
        phrase=get_important(self.total.split()[-QQQ:-1])
        print("phrase",phrase)
        self.url = get_video(phrase) or self.url
        print("url",self.url)
        return self.url

    def on_recognizing(self, args):
        self.speech_thing = (args.result.text)
        self.total+=f" {self.speech_thing}"
        #print(self.speech_thing)

    async def recognize(self):
        print("Recognizing speech")
        speech_recognizer.recognizing.connect(self.on_recognizing)
        speech_recognizer.start_continuous_recognition_async()
        while True:
            await asyncio.sleep(0)
