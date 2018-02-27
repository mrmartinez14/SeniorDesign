from enum import Enum

class states(Enum):
    straight_turn_s = 0
    straight_turn_l = 1
    straight_turn_r = 2
    right_turn_r = 3
    right_turn_s = 4
    left_turn_l = 5
    left_turn_s = 6

class state_machine:


    def __init__(self):
        current_state = states.straight_turn_s
        next_state = states.straight_turn_s
