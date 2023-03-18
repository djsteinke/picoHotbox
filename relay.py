import utime
from machine import Pin


class Relay(object):
    def __init__(self, pin, name, led):
        self._on = False
        self._pin = pin
        self._gpio = None
        self._run_time = 0
        self._callback = None
        self._start_time = 0
        self._name = name
        self._led = led
        self.setup_pin()

    def check(self):
        # self.log("check()")
        if self._on and self._start_time + self._run_time < utime.time():
            self.off()

    def on(self):
        if self._run_time == 0:
            self._run_time = 300
        self._on = True
        self._start_time = utime.time()
        self._gpio.on()
        self._led.blink()
        self.log(f"on() pin: {self._pin}, startTime: {self._start_time}, runTime: {self._run_time}")

    def off(self):
        self._on = False
        self._gpio.off()
        self._led.blink()
        self.log(f"off() pin: {self._pin}, endTime: {utime.time()}, runTime: {self._run_time}")
        if self._callback is not None:
            self._callback()

    def setup_pin(self):
        self.log(f"setup_pin() pin: {self._pin}")
        self._gpio = Pin(self._pin, Pin.OUT)
        self._gpio.off()
        self._led.blink()

    def log(self, msg):
        tmp = 1
        print(f"Relay() -- {self._name} : {msg}")

    @property
    def pin(self):
        return self._pin

    @property
    def is_on(self):
        return self._on

    @property
    def run_time(self):
        return self._run_time

    @property
    def callback(self):
        return self._callback

    @callback.setter
    def callback(self, value):
        self._callback = value

    @pin.setter
    def pin(self, value):
        if (self._pin != value) and not self._on:
            self._pin = value
            self.setup_pin()

    @run_time.setter
    def run_time(self, value):
        self._run_time = value
