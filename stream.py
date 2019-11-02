import cv2
url = 'https://billwurtz.com/snail-time.mp4'

#start the video
cap = cv2.VideoCapture(url)
while True:
    try:
        ret, frame = cap.read()
        cv2.imshow("Ignitify", frame)
    except cv2.error:
        break
        
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
