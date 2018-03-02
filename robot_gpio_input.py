from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np
import time
import wiringpi as wpi
from color import colors, WIDTH, HEIGHT
from state_machine import stateMachine

# initialize the camera and grab a reference to the raw camera capture
width = WIDTH
height = HEIGHT
camera = PiCamera()
camera.resolution = (width, height)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(width, height))
state = 'c'
first = True
xCoord = 0
start_button = 21
prox_sensor = 26
count = 0
reset = True
sm = stateMachine()
# allow the camera to warmup
time.sleep(0.1)

# Setup GPIO
wpi.wiringPiSetupGpio()
wpi.pinMode(start_button, wpi.INPUT)
wpi.pinMode(prox_sensor, wpi.INPUT)

cam = colors()

def we_found_it():
    print 'yo'
    sm.do_the_turn()

#wpi.wiringPiISR(prox_sensor, 2, we_found_it)

# Wait for start button
while wpi.digitalRead(start_button) == 0:
    print('wait to start')

sm.get_rolling(.75)
# capture frames from the camera
try:
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        if wpi.digitalRead(start_button) == 0:
            raise KeyboardInterrupt
        if wpi.digitalRead(prox_sensor) == 0:
            we_found_it()

        # grab the raw NumPy array representing the image, then initialize the timestamp
        # and occupied/unoccupied text
        image = frame.array

        if wpi.digitalRead(prox_sensor) == 0:
            we_found_it()

        mask = cam.get_mask(state, image, sm)
        if wpi.digitalRead(prox_sensor) == 0:
            we_found_it()


        xCoord = cam.get_position(mask, sm)
        sm.set_motors(sm.get_next_state(xCoord))
        print(xCoord)

        if wpi.digitalRead(prox_sensor) == 0:
            we_found_it()

        xCoord = 0
        rawCapture.truncate(0)

except KeyboardInterrupt:
    print('Ending program')

finally:
    print('finally')
    sm.kill_motors()
