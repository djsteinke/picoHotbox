from machine import Pin
from time import sleep_ms


class Led(object):
    def __init__(self):
        self._pin = Pin("LED", Pin.OUT)

    def blink(self):
        self._pin.on()
        sleep_ms(100)
        self._pin.off()
