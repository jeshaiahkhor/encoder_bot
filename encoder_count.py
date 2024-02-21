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
spd_a = 1.0
fs = 1


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

# Creating the Motor and Encoder objects
motor = Motor(forward=in1, backward=in2, enable=ena)
enc1 = Encoder(enc_a)

# Forever looping - 
while 1:
    motor.forward(spd_a)
    print("enc1 {}".format(enc1._value))
    sleep(fs)
