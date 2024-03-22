# pygame keyboard 
import pygame
import KeyPressModule as kp
import numpy as np
import cv2

from djitellopy import tello
from time import sleep

kp.init()

me = tello.Tello()
me.connect()

# PARAMETERS
fSpeed = 117/10 # forward speed in cm/s
aSpeed = 360/10 # angular speed in deg/s
interval = 0.25
dInterval = fSpeed * interval
aInterval = aSpeed * interval

x, y = 500, 500 # coordinates
a = 0 # angle
yaw = 0 # yaw
points = [(0, 0), (0, 0)]


def get_keyboard_input():
    global a, yaw, x, y
    lr, fb, ud, yv = 0, 0, 0, 0
    speed = 50
    aspeed = 50
    d = 0

    if kp.getKey('LEFT'):
        lr = -speed
        d = dInterval
        a = -180

    elif kp.getKey('RIGHT'):
        lr = speed
        d = -dInterval
        a = 180

    if kp.getKey('UP'):
        fb = speed
        d = dInterval
        a = 270

    elif kp.getKey('DOWN'):
        fb = -speed
        d = -dInterval
        a = -90

    if kp.getKey('w'):
        ud = speed
    elif kp.getKey('s'):
        ud = -speed

    if kp.getKey('a'):
        yv = -aspeed
        yaw += aInterval

    elif kp.getKey('d'):
        yv = aspeed
        yaw -= aInterval

    if kp.getKey('q'): me.land()
    if kp.getKey('t'): me.takeoff()

    sleep(interval)
    a += yaw
    x += int(d * np.cos(np.radians(a)))
    y += int(d * np.sin(np.radians(a)))

    return [lr, fb, ud, yv, x, y]

def drawPoints(img, points):
    for point in points:
        cv2.circle(img, point, 5, (0, 0, 255), cv2.FILLED)
    cv2.circle(img, points[-1], 8, (255, 255, 0), cv2.FILLED)
    # put text
    cv2.putText(img, f'({(points[-1][0] - 500)/100}, {(points[-1][1] - 500)/100})m',
                (points[-1][0] + 10, points[-1][1] + 30), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 255), 1)
    
    

while True:
    vals = get_keyboard_input()
    me.send_rc_control(vals[0], vals[1], vals[2], vals[3])
    # get battery and height
    print(me.get_battery())
    print(me.get_height())
    # plot opencv
    img = np.zeros((1000, 1000, 3), np.uint8)
    if (points[-1][0] != vals[4] or points[-1][1] != vals[5]):
        points.append((vals[4], vals[5]))
    drawPoints(img, points)
    # show image
    cv2.imshow("Output", img)
    cv2.waitKey(1)
    sleep(0.05)
