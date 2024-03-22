from djitellopy import tello
from time import sleep
import cv2

# Connect to Tello
me = tello.Tello()
me.connect()

# get battery
print(me.get_battery())

# # get image
me.streamon()
while True:
    img = me.get_frame_read().frame
    #resize the image
    img = cv2.resize(img, (240, 240))

    cv2.imshow("Image", img)
    cv2.waitKey(1)
    # sleep(0.5)
