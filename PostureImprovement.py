import cv2
import time
from plyer import notification
import threading


def notify_person():
    notification.notify(
        # title of the notification,
        title="Posture Monitor",
        # the body of the notification
        message="Please change your posture",
        # creating icon for the notification
        # we need to download a icon of ico file format
        app_icon=None,
        # the notification stays for 50sec
        timeout=50
    )
    notify_thread.run()


cascPath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)
notify_thread = threading.Timer(30, notify_person)
notify_thread_on_off = False
video_capture = cv2.VideoCapture(0)
coord1_x = 0
coord1_y = 0
coord2_x = 0
coord2_y = 0
posture_counter = 0
flag = 0
areaFlag = False
areaFrame = 0
count = 0

while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )
    # Draw a rectangle around the faces
    if len(faces) != 0:
        for (x, y, w, h) in faces:
            rect_frame = cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 0), 2)
            count += 1
            if count >= 21:
                if not notify_thread_on_off:
                    notify_thread.start()
                    notify_thread_on_off = True
                if count != 0 and areaFrame > 10000 and areaFlag and w * h > 10000:
                    # checking if the face has gone out of frame
                    if abs(x - coord1_x) >= 20:
                        if notify_thread.is_alive():
                            notify_thread.cancel()
                            notify_thread_on_off = False
                            notify_thread = threading.Timer(30, notify_person)
                if w * h > 10000:
                    areaFlag = True
                    areaFrame = w * h
                    coord1_x = x
                    coord1_y = y
                    coord2_x = x + w
                    coord2_y = y + h
                else:
                    areaFlag = False
            time.sleep(0.1)

    # Display the resulting frame
    cv2.imshow('Volunteer Picture Frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
video_capture.release()
