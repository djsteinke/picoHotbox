import machine
from time import sleep_ms, time


# I2C address
address = 0x38
measure_cmd = [0x30, 0x00]

i2c = machine.I2C(0, scl=machine.Pin(5), sda=machine.Pin(4))

measure_interval = 15


def write_mem(reg, data):
    buf = bytearray()
    for d in data:
        buf.append(d)
    i2c.writeto_mem(address, reg, buf)


def write(data):
    buf = bytearray()
    for d in data:
        buf.append(d)
    i2c.writeto(address, buf)


def read_mem(reg, nbytes=1):
    return i2c.readfrom_mem(address, reg, nbytes)


def read(nbytes=1):
    return i2c.readfrom(address, nbytes)


class TempSensor(object):
    def __init__(self):
        self._temp = 0
        self._temp_f = 0
        self._humid = 0
        self._on = False
        self._last_measure = 0

    def on(self):
        try:
            sleep_ms(500)
            write([0x71])
            state_word = read()
            device_check = read_mem(0x18)
            self._on = state_word == device_check
        except:
            print('failed to start temp sensor')
            self._on = False

    def measure(self):
        if time() - self._last_measure > measure_interval:
            write_mem(0xAC, measure_cmd)
            sleep_ms(250)
            while True:
                ret = read(1)
                if ret[0] & 0x01 == 0:
                    break
                sleep_ms(50)
            data = read(7)
            temp_raw = ((data[3] & 0x0F) << 16) | (data[4] << 8) | data[5]
            self._temp = round((temp_raw / 1048575 * 200) - 50, 2)
            self._temp_f = round(self._temp * 1.8 + 32.0, 2)
            humid_raw = ((data[1] << 16) | (data[2] << 8) | data[3]) >> 4
            self._humid = round(humid_raw / 1048576 * 100, 1)
            self._last_measure = time()
            print('{"c": %0.2f, "f": %0.2f, "h": %0.1f}' % (self._temp, self._temp_f, self._humid))
