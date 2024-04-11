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
original_speed = 0.75
target = 40     # Target no. of ticks per fs duration

kp = 0.005
kd = 0.001
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

# Defining the turning function
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

def straight(robot, left_encoder, right_encoder, speed=0.75, time):
    # Defining parameters
    kp = 

### Creating the Robot and Encoder objects
# Robot object
bot = Robot(left=Motor(forward=in1, backward=in2, enable=ena), right=Motor(forward=in3, backward=in4, enable=enb))
bot.value = (ori_spd_a, ori_spd_b)  # Setting motor speeds

spd_a = ori_spd_a
spd_b = ori_spd_b

# Encoder objects
enc1 = Encoder(enc_a)
enc2 = Encoder(enc_b)

# Forever looping 
count = 0

prev_err = 0
sum_err = 0

while 1:
    # Calculating motor error - motor 1 is the reference, motor 2 will (try) to match it
    err = enc1._value - enc2._value
    print(f'error: {err}')

    # Adding an allowance for error?
    if abs(err) > allowance:
        # Finding the new motor speed (adjustment = error x kp, new_speed = old_speed + adjustment)
        p_comp = err*kp
        d_comp = prev_err*kd
        i_comp = sum_err*ki
        adj = p_comp + d_comp + i_comp
        spd_b += adj
        
        print("p {} d {} i {} total {}".format(p_comp, d_comp, i_comp, adj))

        # Setting min and max values to 0 and 1 in case that is exceeded
        spd_b = max(min(1, spd_b), 0)

        # Updating robot speed
        bot.value = (spd_a, spd_b)

        # Printing output of motor speeds
        print("enc1 {} enc2 {} m1 {} m2 {}".format(enc1._value, enc2._value, spd_a, spd_b))
        sleep(fs)

        count += 1
        prev_err = err
        sum_err += err
    elif abs(prev_err) > allowance and abs(err) < allowance:
        bot.value = (ori_spd_a, ori_spd_b)
        print(f'HARD FIX - speeds adjusted; prev err: {prev_err}, err: {err}')
        prev_err = err
