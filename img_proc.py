import numpy as np
import cv2
import wiringpi as wpi

# Camera resolution
WIDTH = 1024
HEIGHT = 576

# GPIO crap


# Define range of color in HSV
lower_red = np.array([160,30,30])
upper_red = np.array([185,255,255])
lower_blue = np.array([100,20,20])
upper_blue = np.array([130,255,255])
lower_yellow = np.array([20,60,60])
upper_yellow = np.array([25,200,200])
lower_green = np.array([70,30,30])
upper_green = np.array([90,255,255])

class colors:
    def __init__(self):
        self.count = 0
        self.last = 's'


    def get_mask(self, state, img):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        if state == 'h':
            mask = cv2.inRange(img, lower_green, upper_green)
        elif state == 'c':
            mask = cv2.inRange(img, lower_yellow, upper_yellow)
        elif state == 'b':
            mask = cv2.inRange(img, lower_blue, upper_blue)
        elif state == 'f':
            mask = cv2.inRange(img, lower_red, upper_red)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)
        return mask


    def get_position(self, mask):
        pos = 0
        cnts = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]

        if len(cnts) > 0:
            c = max(cnts, key=cv2.contourArea)
            for i in c.tolist():
                pos = pos + i[0][0]

            pos = pos/len(c)
            if pos < 614:
                self.last = 'r'
            elif pos >= 614 and pos < 820:
                self.last = 's'
            elif pos >= 820:
                self.last = 'l'
            return pos
        else:
            if self.last == 'r':
                return 300
            elif self.last == 's':
                return 800
            elif self.last == 'l':
                self.last = 'll'
                return 1100
            elif self.last == 'll':
                if self.count < 1:
                    self.count = self.count + 1
                    return 1600
                else:
                    self.last = 'lll'
                    return 1600
            elif self.last == 'lll':
                return 1600
