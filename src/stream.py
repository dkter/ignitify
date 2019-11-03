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
            h, w, _ = frame.shape
            cv2.putText(frame, "DISRUPTIVE", (w//2 - 100, h//2), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
            cv2.imshow("Ignitify", frame)
        except cv2.error:
            break

        cv2.waitKey(mspf)
        await asyncio.sleep(0)
    cap.release()


async def get_video(speechrecognizer):
    loop = asyncio.get_event_loop()
    url = await speechrecognizer.get_video()
    return await loop.run_in_executor(None, cv2.VideoCapture, url)


async def play_videos(speechrecognizer):
    url = random.choice(speech2.videos)
    cap = cv2.VideoCapture(url)
    loop = asyncio.get_event_loop()
    while True:
        print("Getting video !!!!!!!!!!!!!!!!!!!")
        cap_task = asyncio.create_task(get_video(speechrecognizer))
        print("p")
        await play_video(cap)
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