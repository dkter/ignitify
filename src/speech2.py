from xml.etree import ElementTree
import os
from azure.cognitiveservices import speech
import requests
import asyncio
from pixabay_utils import get_video
from text_analysis import get_important
from speech_key import speech_key
import random

from speech import QQQ

videos = [
    "videos/1.mp4",
    "videos/2.mp4",
    "videos/3.mp4",
    "videos/4.mp4",
    "videos/5.mp4",
    "videos/6.mp4",
    "videos/7.mp4",
    "videos/8.mp4",
    "videos/9.mp4",
    "videos/10.mp4",
    "videos/11.mp4",
    "videos/12.mp4",
    "videos/13.mp4",
    "videos/14.mp4",
    "videos/15.mp4",
    "videos/16.mp4",
    "videos/17.mp4",
    "videos/18.mp4",
    "videos/19.mp4",
]

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
    url = random.choice(videos)
    speech_thing = ""
    last_id = 0
    total=""
    async def get_text(self):
        return self.speech_thing

    async def get_video(self):
        phrase=get_important(self.total.split()[-QQQ:-1])
        print("phrase",phrase)
        self.url, self.last_id = get_video(phrase, self.last_id)
        if not self.url:
            self.url = random.choice([v for v in videos if v != self.url])
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
