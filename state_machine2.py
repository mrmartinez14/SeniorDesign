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




def start():
    motors.setSpeeds(0,0)
    motors.enable()
    left = 'y'
    return states.straight_turn_s

def do_the_turn():
    motors.setSpeeds(480,-480)
    time.sleep(.2)
    motors.setSpeeds(-200,-200)

def kill_motors():
    motors.disable()
    motors.setSpeeds(0,0)

def set_motors(state):
    if state == states.straight_turn_s:
        motors.setSpeeds(-200,-180)
    elif state == states.straight_turn_l:
        motors.setSpeeds(0,-480)
    elif state == states.straight_turn_r:
        motors.setSpeeds(-480,0)
    elif state == states.right_turn_r:
        motors.setSpeeds(-480,150)
    elif state == states.right_turn_s:
        motors.setSpeeds(-200,-200)
    elif state == states.left_turn_l:
        motors.setSpeeds(0,-480)
    elif state == states.left_turn_s:
        motors.setSpeeds(-200,-200)

def reset_motors():
    motors.enable()

def get_rolling():
    motors.setSpeeds(-250,-250)
#    time.sleep(duration)
    return

def get_next_state( coord):
    if coord <= 750:
        return states.right_turn_r
    elif coord > 750 and coord <= 1024:
        return states.straight_turn_s
    elif coord > 1500:
        return states.left_turn_l
