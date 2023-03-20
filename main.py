# internal imports
from relay import Relay
from temp_sensor import TempSensor
from wlan import WLAN
from led import Led
import mynetwork

from ufirestore import ufirebaseio
from time import sleep_ms
import _thread
import urequests

#led_relay = Relay(25, "led")
#led_relay.run_time = 5

running = "none"


def update_running(value):
    global running
    running = value
    print(running)
    mynetwork.complete_job()


led = Led()


relay = Relay(25, "test", led)
relay.run_time = 5
start = True

sensor = TempSensor()
sensor.on()

wifi = WLAN()

#ufirebaseio.ping()
#ufirebaseio.login()
#mynetwork.wifi = wifi
#mynetwork.run_job(job=[ufirebaseio.login, []])
#mynetwork.run_job([ufirebaseio.get, ["hotbox/running.json", update_running, True]])

#_thread.start_new_thread(ufirebaseio.ping, [])
if wifi.connected:
    try:
        response = urequests.request("GET", "https://rn5notifications-default-rtdb.firebaseio.com/hotbox/ping.json")
        print(response)
    except:
        pass

while True:
    wifi.check()
    sensor.measure()

    if not relay.is_on:
        sleep_ms(1000)
        relay.on()

    relay.check()

    sleep_ms(100)
