import RPi.GPIO as GPIO

###
#Pin 1 is for forward
#Pin 2 is for backward
#Motors 0 and 1 are left
#Motors 2 and 3 are right
###
class Motors:
    def __init__(self, pinL1, pinL2, pinR1, pinR2, freq=60):
        if GPIO.getmode() is None:
            GPIO.setmode(GPIO.BCM)
        self.pins = [pinL1, pinL2, pinR1, pinR2]
        self.freq = freq
        GPIO.setup(self.pins[0], GPIO.OUT)
        GPIO.setup(self.pins[1], GPIO.OUT)
        GPIO.setup(self.pins[2], GPIO.OUT)
        GPIO.setup(self.pins[3], GPIO.OUT)
        motor1 = GPIO.PWM(self.pins[0], self.freq)
        motor2 = GPIO.PWM(self.pins[1], self.freq)
        motor3 = GPIO.PWM(self.pins[2], self.freq)
        motor4 = GPIO.PWM(self.pins[3], self.freq)
        self.motors = [motor1, motor2, motor3, motor4]
        self.forward = 0

    def cleanup(self):
        GPIO.cleanup(self.pins)

    def start(self, forward=True):
        if self.forward is 0:
            if forward is True:
                self.motors[2].start(100)
                self.motors[0].start(100)
                self.forward = 1
            else:
                self.motors[1].start(100)
                self.motors[3].start(100)
                self.forward = 2

    def stop_motors(self):
        for motor in self.motors:
            motor.stop()
        self.forward = 0

    def turn_left(self):
        if self.forward is 0:
            self.motors[1].start(50)
            self.motors[2].start(50)
        elif self.forward is 1:
            self.motors[0].ChangeDutyCycle(0)
        elif forward is 2:
            self.motors[1].ChangeDutyCycle(0)

    def turn_right(self):
        if self.forward is 0:
            self.motors[0].start(50)
            self.motors[3].start(50)
        elif self.forward is 1:
            self.motors[2].ChangeDutyCycle(0)
        elif self.forward is 2:
            self.motors[3].ChangeDutyCycle(0)

    def slight_left(self):
        if self.forward is 0:
            self.motors[1].start(10)
            self.motors[2].start(10)
        elif self.forward is 1:
            self.motors[0].ChangeDutyCycle(90)
        elif self.forward is 2:
            self.motors[1].ChangeDutyCycle(90)

    def slight_right(self):
        if self.forward is 0:
            self.motors[0].start(10)
            self.motors[3].start(10)
        elif self.forward is 1:
            self.motors[2].ChangeDutyCycle(90)
        elif forward is 2:
            self.motors[3].ChangeDutyCycle(90)

    def straight(motors, forward):
        if self.forward is 0:
            for motor in self.motors:
                motor.stop()
        elif self.forward is 1:
            self.motors[0].ChangeDutyCycle(100)
            self.motors[2].ChangeDutyCycle(100)
        elif self.forward is 2:
            self.motors[1].ChangeDutyCycle(100)
            self.motors[3].ChangeDutyCycle(100)

