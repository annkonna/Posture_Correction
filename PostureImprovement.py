import cv2
import time
import threading
from plyer import notification


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


cascPath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)
notif_time = threading.Timer(600, notify_person)
video_capture = cv2.VideoCapture(0)
coord1_x = 0
coord1_y = 0
coord2_x = 0
coord2_y = 0
timer_on = False
flag = 0
areaFlag = False
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
            print(count)
            if flag == 0:
                flag = 1
            else:
                pass
            if count >= 11:
                if not timer_on:
                    notif_time.start()
                    timer_on = True
                if coord1_x != 0 and w * h > 20000 and areaFlag != False:
                    if abs(x - coord1_x) >= 20:
                        print(abs(x - coord1_x))
                        print(x)
                        print(coord1_x)
                        print("True")
                        notif_time.cancel()
                        notif_time.start()
                if w * h > 20000:
                    areaFlag = True
                    coord1_x = x
                    coord1_y = y
                    coord2_x = x + w
                    coord2_y = y + h
                    print(coord1_x, coord1_y, coord2_x, coord2_y)
                    print(w * h)
                else:
                    areaFlag = False
            time.sleep(0.1)
            # compare(rect_frame, prev_frame)

    # Display the resulting frame
    cv2.imshow('Volunteer Picture Frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
video_capture.release()
