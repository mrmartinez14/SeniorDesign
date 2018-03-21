from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np
import time
from img_proc import colors, WIDTH, HEIGHT

# initialize the camera and grab a reference to the raw camera capture
width = WIDTH
height = HEIGHT
def start_camera():
    global camera
    camera = PiCamera()
    camera.resolution = (width, height)
    camera.framerate = 32
    global rawCapture
    rawCapture = PiRGBArray(camera, size=(width, height))
    time.sleep(0.1)
    global cam
    cam = colors()

state = 'c'
first = True
xCoord = 0
start_button = 21
prox_sensor = 26
count = 0
reset = True
# allow the camera to warmup

# Setup GPIO



def get_frame():
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
#        if i == 0:
         return frame.array

def get_mask(img):
    return cam.get_mask(state,img)

def get_position(mask):
    return cam.get_position(mask)

def clean_up():
    rawCapture.truncate(0)

def stuff_we_wont_use():
    # capture frames from the camera
    try:
        for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

        # grab the raw NumPy array representing the image, then initialize the timestamp
        # and occupied/unoccupied text
            image = frame.array

            mask = cam.get_mask(state, image)

            xCoord = cam.get_position(mask)

            xCoord = 0
            rawCapture.truncate(0)

    except KeyboardInterrupt:
        print('Ending program')

    finally:
        print('finally')

