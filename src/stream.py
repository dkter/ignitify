import cv2
import time
import asyncio
import random
import speech2


from google.oauth2 import service_account
from google.cloud.speech import enums

videos = [
    "https://billwurtz.com/might-quit.mp4",
    "https://billwurtz.com/wild-frolicking-adventures-of-informational-education.mp4",
    "https://billwurtz.com/at-the-airport-terminal.mp4",
    "https://billwurtz.com/ball-and-stick.mp4"
]
credentials = service_account.Credentials. from_service_account_file(r'C:\Users\dkter\Downloads\My First Project-4397387e7cb5.json')
QQQ=16
# Audio recording parameters
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms

def get_video_blocking():
    print("Get video 1")
    time.sleep(1)
    print("Get video 2")
    return random.choice(videos)


async def play_video(url):
    cap = cv2.VideoCapture(url)

    fps=cap.get(cv2.CAP_PROP_FPS)
    mspf=int(1000/fps)
    clip_length = 5

    loop = asyncio.get_event_loop()

    for frame in range(int(clip_length * fps)):
        try:
            ret, frame = cap.read()
            cv2.imshow("Ignitify", frame)
        except cv2.error:
            break

        cv2.waitKey(mspf)
        await asyncio.sleep(0)
    cap.release()


async def get_video():
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, get_video_blocking)


async def play_videos(speechrecognizer):
    url = videos[0]
    while True:
        print("Getting video !!!!!!!!!!!!!!!!!!!")
        url_task = asyncio.create_task(speechrecognizer.get_video())
        await play_video(url)
        url = await url_task


# print("START")
# # See http://g.co/cloud/speech/docs/languages
# # for a list of supported languages.
# language_code = 'en-US'  # a BCP-47 language tag

# client = speech.speech.SpeechClient(credentials=credentials)
# print("CLIENTED")
# config = speech.types.RecognitionConfig(
#     encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
#     sample_rate_hertz=RATE,
#     language_code=language_code)
# streaming_config = speech.types.StreamingRecognitionConfig(
#     config=config,
#     interim_results=True)

# print("WITH")
# with speech.MicrophoneStream(RATE, CHUNK) as stream:
#     audio_generator = stream.generator()
#     requests = (speech.types.StreamingRecognizeRequest(audio_content=content)
#                 for content in audio_generator)
#     responses = client.streaming_recognize(streaming_config, requests)

#     # Now, put the transcription responses to use.
#     speechrecognizer = speech.SpeechRecognizer()

loop = asyncio.get_event_loop()
speechrecognizer = speech2.SpeechRecognizer()
loop.run_until_complete(asyncio.gather(
    speechrecognizer.recognize(),
    play_videos(speechrecognizer)
))

cv2.destroyAllWindows()