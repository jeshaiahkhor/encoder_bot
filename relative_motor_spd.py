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
spd_a = 0.75
spd_b = 0.75
target = 40     # Target no. of ticks per fs duration

kp = 0.005
kd = 0
ki = 0

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
bot.value = (spd_a, spd_b)  # Setting motor speeds

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
    print(err)


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
