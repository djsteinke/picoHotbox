import time
import network
import usocket


interval = 60


def is_up(wifi):
    try:
        if wifi.isconnected():
            usocket.getaddrinfo('www.google.com', 80, 0, usocket.SOCK_STREAM)
            return True
        else:
            raise Exception
    except:
        return False


class WLAN(object):
    def __init__(self):
        self._wlan = network.WLAN(network.STA_IF)
        self._last_check = 0
        self.check()

    def check(self):
        if time.time() - self._last_check > interval:
            if not is_up(self._wlan):
                self._wlan.connect(ssid, password)
                print("Trying to connect to Wi-Fi", end="...")
                i = 0
                while i < 5:
                    if is_up(self._wlan):
                        break
                    i += 1
                    print(".", end="")
                    time.sleep(1)
            print("connected: ", self._wlan.isconnected())
            self._last_check = time.time()

    @property
    def connected(self):
        return self._wlan.isconnected()
