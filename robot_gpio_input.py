from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import numpy as np
import time
import wiringpi as wpi
import color
from state_machine import stateMachine

# initialize the camera and grab a reference to the raw camera capture
width = color.WIDTH
height = color.HEIGHT
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

# Wait for start button
while wpi.digitalRead(start_button) == 1:
    print('wait to start')

#sm.get_rolling(.25)
# capture frames from the camera
try:
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        if wpi.digitalRead(start_button) == 1:
            raise KeyboardInterrupt

        # grab the raw NumPy array representing the image, then initialize the timestamp
        # and occupied/unoccupied text
        image = frame.array

        mask = color.get_mask(state, image)

        xCoord = color.get_position(mask)
        sm.set_motors(sm.get_next_state(xCoord))
        print(xCoord)

 #       if wpi.digitalRead(prox_sensor) == 0 and reset == True:
 #           if state == 'h':
 #               state = 'c'
 #               reset = False
 #           elif state == 'c':
 #               if count == 0:
 #                   count = 1
 #                   reset = False
 #               elif count == 1:
 #                   count = 2
 #                   state = 'b'
 #                   reset = false
 #               elif count == 2:
 #                   count = 3
 #                   reset = False
 #               elif count == 3:
 #                   state = 'f'
 #                   reset = False
 #       elif wpi.digitalRead(prox_sensor) == 0 and reset = False:
            #do motor stuff to turn
 #       elif wpi.digitalRead(prox_sensor) == 1 and reset = False:
            #do motor stuff to go straight
#            reset = True

        xCoord = 0
        rawCapture.truncate(0)

except KeyboardInterrupt:
    print('Ending program')

finally:
    print('finally')
    sm.kill_motors()
