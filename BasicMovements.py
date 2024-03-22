import djitellopy as tello
import cv2 as cv
from time import sleep

# Connect to Tello
me = tello.Tello()
me.connect()

# get battery
print(me.get_battery())

# get height
print(me.get_height())

# # # takeoff tello
# me.takeoff()
# sleep(5)

# # # set speed
# me.send_rc_control(0, 50, 0, 0);
# # me.send_rc_control(0, 0, 0, 30)
# sleep(2)

# # me.move_up(100)
# # sleep(2)
# me.send_rc_control(0, 0, 0, 0)
# me.land()







