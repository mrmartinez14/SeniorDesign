from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import numpy as np
import time
from dual_mc33926_rpi import motors, MAX_SPEED

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))
state = 'h'
first = True
print('a')
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
print('b')
# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    print('c')
    if first:
        motors.enable()
        motors.setSpeeds(MAX_SPEED, MAX_SPEED)
    # grab the raw NumPy array representing the image, then initialize the timestamp
    # and occupied/unoccupied text
    print('d')
    image = frame.array

    # Convert BGR to HSV
    hsv = image #cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    print('e')
    if state == 'h':
        mask = cv2.inRange(hsv, lower_green, upper_green)
    if state == 'c':
        mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
    if state == 'b':
        mask = cv2.inRange(hsv, lower_blue, upper_blue)
    if state == 'f':
        mask = cv2.inRange(hsv, lower_red, upper_red)

    res = cv2.bitwise_and(image, image, mask=mask)

    if state == 'h':
        if 1 in res[:320,:]:
            print("y")

    rawCapture.truncate(0)

    #if k == 27:
        #break

cv2.destroyAllWindows()

