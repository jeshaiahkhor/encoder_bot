### Importing libraries
from gpiozero import Motor, DigitalInputDevice
from time import sleep

### Defining constants
# Pins
in1 = 17 
in2 = 27
ena = 18
enc_a = 26

# Constants
spd_a = 0.25
fs = 1


# Defining the encoder
#class Encoder(object):
#    def __init__(self, pin):
#        self.value = 0
#        enc1 = DigitalInputDevice(enc_a)
#        enc1.when_activated = self.increment
#    def increment(self):
#        self.value += 1
#        print(self.value)

enc1 = DigitalInputDevice(pin = enc_a, pull_up = None, active_state = True)

# Creating the Motor and Encoder objects
motor = Motor(forward=in1, backward=in2, enable=ena)
#enc1 = Encoder(enc_a)

# Forever looping - 
while 1:
    motor.forward(spd_a)
    print("enc1 {}".format(enc1.value))
    sleep(fs)
