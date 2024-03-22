from djitellopy import tello
import SpeechtoText as stt
from time import sleep
import cv2

SPEED = 15
VOICE_COMMANDS = {
    "take off": (0, 0, SPEED, 0),
    "landing": (0, 0, 0, 0),
    "go up": (0, 0, SPEED, 0),
    "go down": (0, 0, -SPEED, 0),
    "go left": (-SPEED, 0, 0, 0),
    "go right": (SPEED, 0, 0, 0),
    "forward": (0, SPEED, 0, 0),
    "backward": (0, -SPEED, 0, 0),
    "clockwise": (0, 0, 0, SPEED),
    "counter clockwise": (0, 0, 0, -SPEED),
}

me = tello.Tello()
me.connect()
me.streamon()

def voice_control():
    text = stt.speech_to_text().lower()
    for command, action in VOICE_COMMANDS.items():
        if command in text:
            if command == "take off":
                me.takeoff()
            elif command == "landing":
                me.land()
            return action
    return 0, 0, 0, 0

while True:
    try:
        lr, fb, ud, yv = voice_control()
        me.send_rc_control(lr, fb, ud, yv)
        sleep(0.05)

        # stream video
        img = me.get_frame_read().frame
        img = cv2.resize(img, (360, 240))
        cv2.imshow("Image", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            me.land()
            break
    except Exception as e:
        print(f"Error in voice control: {e}")
        break