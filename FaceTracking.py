# import libraries
import cv2
import numpy as np
from djitellopy import tello
from time import sleep

fbRange = [6200, 6800]
pid = [0.4, 0.4, 0]
pError = 0

# connect tello
me = tello.Tello()
me.connect()

# find face
def find_face(img):
    faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(imgGray, 1.1, 4)
    myFaceListC = []
    myFaceListArea = []
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cx = x + w // 2
        cy = y + h // 2
        area = w * h
        # create circle at center of face
        cv2.circle(img, (cx, cy), 5, (0, 255, 0), cv2.FILLED)
        myFaceListArea.append(area)
        myFaceListC.append([cx, cy])
    if len(myFaceListArea) != 0:
        i = myFaceListArea.index(max(myFaceListArea))
        return img, [myFaceListC[i], myFaceListArea[i]]
    else:
        return img, [[0, 0], 0]
    
# def track face using tello
def track_face(me, info, w, pid, pError):
    area = info[1]
    x, y = info[0]
    fb = 0

    # pid
    error = x - w // 2
    speed = pid[0] * error + pid[1] * (error - pError)
    speed = int(np.clip(speed, -100, 100))

    if area > fbRange[0] and area < fbRange[1]:
        fb = 0
    elif area> fbRange[1]:
        fb = -20
    elif area< fbRange[0] and area != 0:
        fb = 20

    if x == 0:
        speed = 0
        error = 0

    me.send_rc_control(0, fb, 0, speed)
    return error
    
    
# video capture using tello
me.streamon()
# takeoff
me.takeoff()
# higher up
me.move_up(100)
sleep(0.5)

while True:
    # get frame
    frame_read = me.get_frame_read()
    myFrame = frame_read.frame
    myFrame = cv2.resize(myFrame, (360, 240))
    myFrame, info = find_face(myFrame)
    pError = track_face(me, info, 360, pid, pError)
    cv2.imshow('My Face', myFrame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        me.land()
        break
