# Importing libraries
from gpiozero import Robot, Motor
from time import sleep

# Defining pins
# Motor 1
in3 = 17
in4 = 27
enb = 18

# Motor 2
in1 = 23
in2 = 24
ena = 25

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
