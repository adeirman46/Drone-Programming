# pygame keyboard 
import pygame
import KeyPressModule as kp

from djitellopy import tello
from time import sleep

kp.init()

me = tello.Tello()
me.connect()

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

    return [lr, fb, ud, yv]

while True:
    vals = get_keyboard_input()
    me.send_rc_control(vals[0], vals[1], vals[2], vals[3])
    # get battery and height
    print(me.get_battery())
    print(me.get_height())
    
    sleep(0.05)
