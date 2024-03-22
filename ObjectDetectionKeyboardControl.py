from ultralytics import YOLO
import supervision as sv
import KeyPressModule as kp

from djitellopy import tello
from time import sleep
import cv2
#import time
from time import time

kp.init()
me = tello.Tello()
me.connect()

# load the model
model = YOLO("yolov8n.pt")

# box annotator
bbox_annotator = sv.BoxAnnotator()

def get_keyboard_input():
    lr, fb, ud, yv = 0, 0, 0, 0
    speed = 50
    if kp.getKey('LEFT'): lr = -speed
    elif kp.getKey('RIGHT'): lr = speed

    if kp.getKey('UP'): fb = speed
    elif kp.getKey('DOWN'): fb = -speed

    if kp.getKey('w'): ud = speed
    elif kp.getKey('s'): ud = -speed

    if kp.getKey('a'): yv = -speed
    elif kp.getKey('d'): yv = speed

    if kp.getKey('q'): me.land()
    if kp.getKey('t'): me.takeoff()

    # save image if 'i' is pressed
    if kp.getKey('i'):
        img = me.get_frame_read().frame
        img = cv2.resize(img, (360, 240))
        cv2.imwrite(f'Images/{time()}.jpg', img)
        sleep(0.3)
    
    return [lr, fb, ud, yv]

me.streamon()
while True:
    vals = get_keyboard_input()
    me.send_rc_control(vals[0], vals[1], vals[2], vals[3])
    sleep(0.05)
    # get battery and height
    print(me.get_battery())
    print(me.get_height())
    
    # stream video
    img = me.get_frame_read().frame
    #resize the image
    img = cv2.resize(img, (360, 240))
    # change bgr to rgb
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # detect objects
    result = model(img)[0]
    # detection
    detection = sv.Detections.from_yolov8(result)
    # confidence 80%
    detection = detection[detection.confidence > 0.8]
    labels = [
        result.names[class_id]
        for class_id in detection.class_id
    ]
    frame = bbox_annotator.annotate(img, detection, labels)
    # display the image
    cv2.imshow("Image", frame)
    # q for land
    if cv2.waitKey(1) & 0xFF == ord('q'):
        me.land()
        break



