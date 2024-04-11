##### Tests PID control for straight-line motion #####

### Importing libraries
from gpiozero import Motor, Robot, DigitalInputDevice
from time import sleep

### Defining constants
# Pins
in1 = 17 
in2 = 27
in3 = 23
in4 = 24

ena = 18
enb = 25

enc_a = 26
enc_b = 16

# Constants
ori_spd_a = 0.75
ori_spd_b = 0.75
target = 40     # Target no. of ticks per fs duration

kp = 0.05
kd = 0
ki = 0

allowance = 2

fs = 0.5

# Defining the Encoder object
class Encoder(object):
    def __init__(self, pin):
        self._value = 0
        self.encoder = DigitalInputDevice(pin)
        self.encoder.when_activated = self._increment
        self.encoder.when_deactivated = self._increment
    def reset(self):
        self._value = 0
    def _increment(self):
        self._value += 1
        #print(self._value)
        
    @property
    def value(self):
        return self._value

### Creating the Robot and Encoder objects
# Robot object
bot = Robot(left=Motor(forward=in1, backward=in2, enable=ena), right=Motor(forward=in3, backward=in4, enable=enb))
#bot.value = (ori_spd_a, ori_spd_b)  # Setting motor speeds

spd_a = ori_spd_a
spd_b = ori_spd_b

# Encoder objects
enc1 = Encoder(enc_a)
enc2 = Encoder(enc_b)

# Defining the right-turn function (assumes stop before turn)
def turn(robot, direction, left_encoder, right_encoder, default_speed=0.75):
    # Setting no. of encoder ticks required (trial & error)
    turn_limit = 28
    
    # Resets the current count of both encoders
    left_encoder.reset()
    right_encoder.reset()

    # Sets the initial speeds of the robot
    left_speed = default_speed 
    right_speed = default_speed

    # Handling right turns
    if direction == 'right':
        # Sets the right motor speed to 0 (allows right turn)
        right_speed = 0
        robot.value = (left_speed, right_speed)

        # Allowing to run while turn angle not reached
        while left_encoder._value - right_encoder._value < turn_limit:
            #print(f'enc1: {enc1._value}, enc2: {enc2._value}\n')
            sleep(0.01)
    elif direction == 'left':
        # Sets the left motor speed to 0 (allows left turn)
        left_speed = 0
        robot.value = (left_speed, right_speed)

        # Allowing to run while turn angle not reached
        while right_encoder._value - left_encoder._value < turn_limit:
            sleep(0.01)

    # Sets to 0 speed to await next step
    robot.value = (0,0)

print('Starting program...')
sleep(1)

for i in range(1, 9):
    turn(bot, 'right', enc1, enc2)
    print(f'right turn no. {i}')
    sleep(1)

for i in range(1, 9):
    turn(bot, 'left', enc1, enc2)
    print(f'left turn no. {i}')
    sleep(1)
