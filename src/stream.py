import cv2
import time
import asyncio
import random

videos = [
    "https://billwurtz.com/might-quit.mp4",
    "https://billwurtz.com/wild-frolicking-adventures-of-informational-education.mp4",
    "https://billwurtz.com/at-the-airport-terminal.mp4",
    "https://billwurtz.com/ball-and-stick.mp4"
]

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


async def play_videos():
    url = videos[0]
    for i in range(3):
        url_task = asyncio.create_task(get_video())
        await play_video(url)
        url = await url_task


loop = asyncio.get_event_loop()

loop.run_until_complete(play_videos())


cv2.destroyAllWindows()