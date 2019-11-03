import cv2
import time
import asyncio
import random
import speech2

QQQ=16
# Audio recording parameters
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms

def get_video_blocking():
    print("Get video 1")
    time.sleep(1)
    print("Get video 2")
    return random.choice(videos)


async def play_video(cap):
    fps=cap.get(cv2.CAP_PROP_FPS)
    mspf=int(1000/fps)
    clip_length = 2

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
    url = random.choice(speech2.videos)
    cap = cv2.VideoCapture(url)
    loop = asyncio.get_event_loop()
    while True:
        print("Getting video !!!!!!!!!!!!!!!!!!!")
        url_task = asyncio.create_task(speechrecognizer.get_video())
        cap_task = asyncio.ensure_future(loop.run_in_executor(None, cv2.VideoCapture, url))
        print("p")
        await play_video(cap)
        url = await url_task
        cap = await cap_task


cv2.namedWindow("Ignitify", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Ignitify", 1280, 720)

loop = asyncio.get_event_loop()
speechrecognizer = speech2.SpeechRecognizer()
loop.run_until_complete(asyncio.gather(
    speechrecognizer.recognize(),
    play_videos(speechrecognizer)
))

cv2.destroyAllWindows()