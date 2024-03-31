# Importing libraries
from gpiozero import Robot, Motor
from time import sleep

# Defining pins
# Motor 1
in1 = 17
in2 = 27
ena = 18

# Motor 2
in3 = 23
in4 = 24
enb = 25

# Defining robot instance
robot = Robot(left=Motor(forward=in1, backward=in2, enable=ena), right=Motor(forward=in3, backward=in4, enable=enb))

# Testing all basic robot movements
while 1:
    robot.forward()
    sleep(2)
    robot.stop()
    sleep(1)
    robot.backward()
    sleep(2)
    robot.stop()
    sleep(1)
    robot.right()
    sleep(2)
    robot.stop()
    sleep(1)
    robot.left()
    sleep(2)
    robot.stop()
    sleep(1)
    robot.forward(0.5)
    sleep(2)
    robot.stop()
    sleep(1)
