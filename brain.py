import motorControl
import time
import images

motors = motorControl.Motors(22, 10, 17, 27)
print(motors.forward)
motors.start()
print(motors.forward)
time.sleep(10)
motors.stop_motors()
print(motors.forward)
motors.cleanup()
