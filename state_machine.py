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
        self.motors = motors
        self.current_state = states.straight_turn_s
        self.motors.setSpeeds(0,0)
        self.motors.enable()
        self.count = 0

    def update_state(self, coord, motors_on):
#        if self.count < 10:
#            self.count = self.count + 1
        if self.current_state == states.straight_turn_s:
            self.current_state = get_next_state(coord)
        elif self.current_state == states.straight_turn_l:
            self.current_state = states.straight_turn_s
        elif self.current_state == states.straight_turn_r:
            self.current_state = states.straight_turn_s
        elif self.current_state == states.left_turn_l:
            self.current_state = states.left_turn_s
        elif self.current_state == states.right_turn_r:
            self.current_state = states.right_turn_s
        elif self.current_state == states.left_turn_s:
            self.current_state = states.straight_turn_r
#            self.count = 0
        elif self.current_state == states.right_turn_s:
            self.current_state = states.straight_turn_l
#            self.count = 0
        elif self.current_State == states.straight_turn_r:
            self.current_state = states.straight_turn_s
        elif self.current_State == states.straight_turn_l:
            self.current_state = states.straight_turn_s
        if motors_on:
            self.set_motors(self.current_state)
#        else:
        print self.current_state

    def kill_motors(self):
        self.motors.disable()
        self.motors.setSpeeds(0,0)

    def set_motors(self, state):
        if state == states.straight_turn_s:
            self.motors.setSpeeds(-250,-250)
        elif state == states.straight_turn_l:
            self.motors.setSpeeds(150,-480)
        elif state == states.straight_turn_r:
            self.motors.setSpeeds(-480,150)
        elif state == states.right_turn_r:
            self.motors.setSpeeds(-480,150)
        elif state == states.right_turn_s:
            self.motors.setSpeeds(-250,-250)
        elif state == state.left_turn_l:
            self.motors.setSpeeds(150,-480)
        elif state == state.left_turn_s:
            self.motors.setSpeeds(-250,-250)

    def reset_motors(self):
        self.motors.enable()

    def get_rolling(self, duration):
        self.motors.setSpeeds(-250,-250)
        time.sleep(duration)
        return

    def get_next_state(self, coord):
        if coord <= 614:
            return states.right_turn_r
        elif coord > 614 and coord <= 820:
            return states.straight_turn_s
        elif coord > 820:
            return states.left_turn_l
