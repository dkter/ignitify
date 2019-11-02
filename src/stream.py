import cv2

from src.shutterstock_utils import get_video

url = get_video("url")

#start the video
cap = cv2.VideoCapture(url)

fps=cap.get(cv2.CAP_PROP_FPS)
mspf=int(1000/fps)
while True:
    try:
        ret, frame = cap.read()
        cv2.imshow("Ignitify", frame)
    except cv2.error:
        break
        
    if cv2.waitKey(mspf) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
