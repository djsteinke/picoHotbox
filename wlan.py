import time
import network


ssid = "DandK"
password = "loveeats"
interval = 60


class WLAN(object):
    def __init__(self):
        self._wlan = network.WLAN(network.STA_IF)
        self._wlan.active(True)
        self._last_check = 0

    def check(self):
        if time.time() - self._last_check > interval:
            if not self._wlan.isconnected():
                self._wlan.connect(ssid, password)
                print("Trying to connect to Wi-Fi", end="...")
                i = 0
                while i < 5:
                    if self._wlan.isconnected():
                        break
                    i += 1
                    print(".", end="")
                    time.sleep(1)
            print("connected: ", self._wlan.isconnected())
            self._last_check = time.time()

    @property
    def connected(self):
        return self._wlan.isconnected()
