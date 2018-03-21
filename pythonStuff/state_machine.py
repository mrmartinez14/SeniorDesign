from enum import Enum
from dual_mc33926_rpi import motors, MAX_SPEED
import time

class states(Enum):
    straight_turn_s = 0
    straight_turn_l = 1
    straight_turn_r = 2
    right_turn_r = 3
    right_turn_s = 4
    left_turn_l = 5
    left_turn_s = 6
    turn = 7

class stateMachine:


    def __init__(self):
        self.m1 = 0
        self.motors = motors
        self.current_state = states.straight_turn_s
        self.motors.setSpeeds(0,0)
        self.motors.enable()
        self.left = 'y'

    def do_the_turn(self):
        print 'yo'
        self.motors.setSpeeds(480,-480)
        time.sleep(.75)
        self.motors.setSpeeds(-200,-200)

    def kill_motors(self):
        self.motors.disable()
        self.motors.setSpeeds(0,0)

    def set_motors(self, state):
        if state == states.straight_turn_s:
#            self.m1=-200
            self.motors.setSpeeds(-60,-60)
        elif state == states.straight_turn_l:
            self.motors.setSpeeds(0,-480)
        elif state == states.straight_turn_r:
            self.motors.setSpeeds(-280,0)
        elif state == states.right_turn_r:
#            self.m1=-200
            self.motors.setSpeeds(-300,0)
        elif state == states.right_turn_s:
            self.motors.setSpeeds(-200,-200)
        elif state == states.left_turn_l:
#            if self.m1 <0:
            self.motors.setSpeeds(0,-280)
#                time.sleep(.05)
#                self.m1 = 480
            self.motors.setSpeeds(0,-480)
        elif state == states.left_turn_s:
            self.motors.setSpeeds(-200,-200)

    def reset_motors(self):
        self.motors.enable()

    def get_rolling(self, duration):
        self.motors.setSpeeds(-250,-250)
        time.sleep(duration)
        return

    def get_next_state(self, coord):
        if coord <= 700:
            return states.right_turn_r
        elif coord > 700 and coord <= 1024:
            return states.straight_turn_s
        elif coord >1024:
            return states.left_turn_l
