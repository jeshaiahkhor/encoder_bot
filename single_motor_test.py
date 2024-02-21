from gpiozero import Motor
from time import sleep


motor = Motor(forward=17, backward=27, enable=18)

while 1:
    motor.forward()
    sleep(5)
    motor.stop()
    sleep(1)
    motor.backward()
    sleep(5)
    motor.stop()
    sleep(1)
