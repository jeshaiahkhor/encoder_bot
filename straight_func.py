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


# Encoder objects
enc1 = Encoder(enc_a)
enc2 = Encoder(enc_b)


def straight(robot, left_encoder, right_encoder, speed=0.75, runtime=1, kp=0.005, kd=0.001, ki=0, allowance=2, fs=0.1):
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
        print(f'error: {err}')

        # Adding an allowance for error
        if abs(err) > allowance:
            # Finding the new motor speed (adjustment = error x kp, new_speed = old_speed + adjustment)
            p_comp = err*kp
            d_comp = prev_err*kd
            i_comp = sum_err*ki
            adj = p_comp + d_comp + i_comp
            right_speed += adj
            
            print("p {} d {} i {} total {}".format(p_comp, d_comp, i_comp, adj))

            # Setting min and max values to 0 and 1 in case that is exceeded
            right_speed = max(min(1, right_speed), 0)

            # Updating robot speed
            bot.value = (left_speed, right_speed)

            # Printing output of motor speeds
            print("enc1 {} enc2 {} m1 {} m2 {}".format(left_encoder._value, right_encoder._value, left_speed, right_speed))
            sleep(fs)

            count += 1
            prev_err = err
            sum_err += err
        elif abs(prev_err) > allowance and abs(err) < allowance:
            bot.value = (speed, speed)
            print(f'HARD FIX - speeds adjusted; prev err: {prev_err}, err: {err}')
            prev_err = err

    # Resetting encoder counts for next action
    left_encoder.reset()
    right_encoder.reset()

print('Testing straight line function...')
straight(bot, enc1, enc2, speed=0.5)
straight(bot, enc1, enc2, speed=0.75)
straight(bot, enc1, enc2, speed=1.0)
print(f'enc1: {enc1._value}, enc2: {enc2._value}')
