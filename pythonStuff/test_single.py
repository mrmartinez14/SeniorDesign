#!/bin/bash

# import necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import numpy as np
import time
import cv2

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640,480))

# allow the camera to warm up
time.sleep(0.1)

# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # grab the raw NumPy array representing the image, then initialize the timestamp
    # and occupied/unoccupied text
    image = frame.array

    # Convert BGR to HSV
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define range of color in HSV
    lower_red = np.array([160,30,30])
    upper_red = np.array([185,255,255])
    lower_blue = np.array([100,20,20])
    upper_blue = np.array([130,255,255])
    lower_yellow = np.array([25,30,30])
    upper_yellow = np.array([33,255,255])
    lower_green = np.array([70,30,30])
    upper_green = np.array([90,255,255])


    # Threshold the HSV image to get only red colors
    mask = cv2.inRange(hsv, lower_red, upper_red)
    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
    res = cv2.bitwise_or(mask,mask_blue)
    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
    res = cv2.bitwise_or(mask,res)
    mask = cv2.inRange(hsv, lower_green, upper_green)
    res = cv2.bitwise_or(mask,res)

    # show the frame
    cv2.imshow("Frame", image)
    cv2.imshow("mask", res)
    key = cv2.waitKey(5) & 0xFF

    # Clear the stream in preparation for the next frame
    frame.truncate(0)

    # if the 'esc' key was pressed, break from the loop
    if key == 27:
        break

cv2.destroyAllWindows()
