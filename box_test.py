##### Tests PID control for straight-line motion #####

### Importing libraries
from gpiozero import Motor, Robot, DigitalInputDevice
from time import sleep
import time

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

fs = 0.1

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


# Encoder objects
enc1 = Encoder(enc_a)
enc2 = Encoder(enc_b)


def straight(robot, left_encoder, right_encoder, speed=0.5, runtime=1, kp=0.01, kd=0.005, ki=0, allowance=2, fs=0.1):
    # Setting initial counter values    
    count = 0
    prev_err = 0
    sum_err = 0

    # Starting the motors running (at default speeds)
    left_speed = speed
    right_speed = speed
    robot.value = (left_speed, right_speed)

    # Running for set amount of time
    t_end = time.time() + runtime
    while time.time() < t_end:
        # Calculating motor error - motor 1 is the reference, motor 2 will (try) to match it
        err = left_encoder._value - right_encoder._value
        #print(f'error: {err}')

        # Adding an allowance for error
        if abs(err) > allowance:
            # Finding the new motor speed (adjustment = error x kp, new_speed = old_speed + adjustment)
            p_comp = err*kp
            d_comp = prev_err*kd
            i_comp = sum_err*ki
            adj = p_comp + d_comp + i_comp
            right_speed += adj
            
            #print("p {} d {} i {} total {}".format(p_comp, d_comp, i_comp, adj))

            # Setting min and max values to 0 and 1 in case that is exceeded
            right_speed = max(min(1, right_speed), 0)

            # Updating robot speed
            bot.value = (left_speed, right_speed)

            # Printing output of motor speeds
            # print("enc1 {} enc2 {} m1 {} m2 {}".format(left_encoder._value, right_encoder._value, left_speed, right_speed))
            sleep(fs)

            count += 1
            prev_err = err
            sum_err += err
        elif abs(prev_err) > allowance and abs(err) < allowance:
            bot.value = (speed, speed)
            #print(f'HARD FIX - speeds adjusted; prev err: {prev_err}, err: {err}')
            prev_err = err

    # Stop motors
    bot.value = (0,0)
    sleep(0.5)
    
    # Resetting encoder counts for next action
    left_encoder.reset()
    right_encoder.reset()


# Defining turning function
def turn(robot, direction, left_encoder, right_encoder, default_speed=0.5):
    # Setting no. of encoder ticks required (trial & error)
    turn_limit = 29
    
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
            # print(f'enc1: {enc1._value}, enc2: {enc2._value}\n')
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
    sleep(0.5)

    # Resetting encoder counts for next action
    left_encoder.reset()
    right_encoder.reset()

# Starting main program\
input()
print('Testing straight line function...')
sleep(1)

print('Starting')
straight(bot, enc1, enc2, runtime=2)

print('Turning right')
turn(bot, 'right', enc1, enc2)

print('Going straight')
straight(bot, enc1, enc2)

print('Turning right')
turn(bot, 'right', enc1, enc2)

print('Going straight')
straight(bot, enc1, enc2, runtime=2)

print('Turning left')
turn(bot, 'left', enc1, enc2)

