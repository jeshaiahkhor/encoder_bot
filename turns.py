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
bot.value = (ori_spd_a, ori_spd_b)  # Setting motor speeds

spd_a = ori_spd_a
spd_b = ori_spd_b

# Encoder objects
enc1 = Encoder(enc_a)
enc2 = Encoder(enc_b)

# Defining the right-turn function
def turn(robot, direction):
    enc1.reset()
    enc2.reset()
    spd_a = ori_spd_a 
    spd_b = ori_spd_b
    
    if direction == 'right':
        spd_b = 0
        robot.value = (spd_a, spd_b)
        while enc1._value - enc2._value < 28:
            print(f'enc1: {enc1._value}, enc2: {enc2._value}\n')
            sleep(0.01)

    robot.value = (0,0)
    #spd_a = ori_spd_a
    #spd_b = ori_spd_b

    #bot.value(spd_a, spd_b)

for i in range(1, 9):
    turn(bot, 'right')
    print(f'turn no. {i}')
    sleep(1)
