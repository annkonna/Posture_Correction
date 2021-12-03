import cv2
import time
from plyer import notification
import threading


def notify_person():
    notification.notify(
        # title of the notification,
        title="Posture Monitor",
        # the body of the notification
        message="Recommend Changing your Posture",
        # creating icon for the notification
        app_icon=None,
        # the notification stays for 50sec
        timeout=50
    )
    notify_thread.run()


cascPath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)
notify_thread = threading.Timer(600, notify_person)
# this is to check if the notification thread has started (defaulted to false)
notify_thread_on_off = False
# this is to check if there has been a posture change (defaulted to false)
posture_change = False
video_capture = cv2.VideoCapture(0)
# this is to calculate the number of seconds (upto atleast 30 seconds) ever since the person made a significant
# posture change (defaulted to 0)
counter_30sec = 0
# this is to save the x coordinate of the face frame detected (defaulted to 0)
coord1_x = 0
# this is to save the previous x coordinate of the face frame detected (defaulted to 0)
checker_x = 0
# this is to check if the area of the face frame detected is accurate (defaulted to false)
areaFlag = False
# this is to calculate the area of the face frame detected (defaulted to 0)
areaFrame = 0
# this is to calculate the number of frames ever since the program started (defaulted to 0)
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
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 255, 0), 2)
            count += 1
            # giving the person a few seconds to settle after the program has started
            if count >= 45:
                # start the notification thread after checking if it had stopped or hadn't started
                if not notify_thread_on_off:
                    # starting the notification thread
                    notify_thread.start()
                    notify_thread_on_off = True
                # verifying the current and previous frame is accurate
                if areaFrame > 19000 and areaFlag and w * h > 19000:
                    # checking if the face has gone out of frame
                    if abs(x - coord1_x) >= 15 or posture_change:
                        if not posture_change:
                            posture_change = True
                            # saving the person's previous posture
                            checker_x = coord1_x
                            counter_30sec += 1
                        else:
                            if abs(x - coord1_x) < 15:
                                # checking if the person is in the new position for atleast 30 seconds.
                                if counter_30sec == 300:
                                    # stop the notification thread after checking if it had started before
                                    if notify_thread.is_alive():
                                        notify_thread.cancel()
                                        notify_thread_on_off = False
                                        notify_thread = threading.Timer(600, notify_person)
                                    counter_30sec = 0
                                    posture_change = False
                                else:
                                    counter_30sec += 1
                            else:
                                # checking if the person went back to their saved posture
                                if abs(x - checker_x) >= 15:
                                    counter_30sec += 1
                                else:
                                    counter_30sec = 0
                                    posture_change = False
                # verifying the face frame detection is accurate
                if w * h > 19000:
                    areaFlag = True
                    areaFrame = w * h
                    coord1_x = x
                else:
                    areaFlag = False
            time.sleep(0.1)

    # Display the resulting frame
    cv2.imshow('Volunteer Picture Frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
video_capture.release()
