from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import numpy as np
import time
from dual_mc33926_rpi import motors, MAX_SPEED
import wiringpi as wpi

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))
state = 'c'
first = True
xCoord = 0
start_button = 21
prox_sensor = 26
count = 0
reset = True

# Define range of color in HSV
lower_red = np.array([160,30,30])
upper_red = np.array([185,255,255])
lower_blue = np.array([100,20,20])
upper_blue = np.array([130,255,255])
lower_yellow = np.array([25,30,30])
upper_yellow = np.array([30,255,255])
lower_green = np.array([70,30,30])
upper_green = np.array([90,255,255])


# allow the camera to warmup
time.sleep(0.1)

# Setup GPIO
wpi.wiringPiSetupGpio()
wpi.pinMode(start_button, wpi.INPUT)
wpi.pinMode(prox_sensor, wpi.INPUT)

# Wait for start button
#while wpi.digitalRead(start_button) == 0:
#    print('wait to start')

# capture frames from the camera
try:
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        if first:
            motors.enable()
            #motors.setSpeeds(MAX_SPEED, MAX_SPEED)
            motors.setSpeeds(0,0)
            first = False
        # grab the raw NumPy array representing the image, then initialize the timestamp
        # and occupied/unoccupied text
        image = frame.array

        # Convert BGR to HSV
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # Get the mask for the current state
        if state == 'h':
            mask = cv2.inRange(hsv, lower_green, upper_green)
        if state == 'c':
            mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
        if state == 'b':
            mask = cv2.inRange(hsv, lower_blue, upper_blue)
        if state == 'f':
            mask = cv2.inRange(hsv, lower_red, upper_red)

        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]

        if len(cnts) > 0:
            c = max(cnts, key=cv2.contourArea)
            for i in c.tolist():
                xCoord = xCoord + i[0][0]
            xCoord = xCoord/len(c)
            print(xCoord)
            if(xCoord > 320):
                motors.setSpeeds(-350,-350)
                print("up")
            elif(xCoord < 320) and (xCoord > 120):
                motors.setSpeeds(0,0)
            else:
                motors.setSpeeds(350,350)
                print("down")
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
    motors.setSpeeds(0,0)
    motors.disable()

