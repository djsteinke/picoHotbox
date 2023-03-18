# internal imports
from relay import Relay
from temp_sensor import TempSensor
from wlan import WLAN
from led import Led

from ufirestore.json import FirebaseJson
from ufirestore import ufirestore
from time import sleep_ms

#led_relay = Relay(25, "led")
#led_relay.run_time = 5

led = Led()


relay = Relay(25, "test", led)
relay.run_time = 5
start = True

sensor = TempSensor()
sensor.on()

wifi = WLAN()



access_token = b'eyJhbGciOiAiUlMyNTYiLCAidHlwIjogIkpXVCIsICJraWQiOiAiYmI3NGE2Yzc4MGYzMjRmYjQ4NTc5YTBiN2IxZmIwZDUzY2JjMjlhOCJ9.eyJpc3MiOiAiZmlyZWJhc2UtYWRtaW5zZGstd3Q4ZjBAcm41bm90aWZpY2F0aW9ucy5pYW0uZ3NlcnZpY2VhY2NvdW50LmNvbSIsICJzdWIiOiAiZmlyZWJhc2UtYWRtaW5zZGstd3Q4ZjBAcm41bm90aWZpY2F0aW9ucy5pYW0uZ3NlcnZpY2VhY2NvdW50LmNvbSIsICJhdWQiOiAiaHR0cHM6Ly9pZGVudGl0eXRvb2xraXQuZ29vZ2xlYXBpcy5jb20vZ29vZ2xlLmlkZW50aXR5LmlkZW50aXR5dG9vbGtpdC52MS5JZGVudGl0eVRvb2xraXQiLCAidWlkIjogImpKWmpySE42OWNXRXUxeXk5MWJERnJFSnpHdTIiLCAiaWF0IjogMTY3OTA3NTYxOCwgImV4cCI6IDE2NzkwNzkyMTh9.LKP9gvQDTiJRYbzwBHG3V3gsr5-w4FYHtW8vO9UxrQN4AKvs5wH6RiIdkLSJXJ0gBccR_5O4WW6CdH4hrxG-80-uwfUqjfunOIOPLpsC-VDAAFaaWNprSUxKb9C1WqaJmx1jPoa3mz6adu0nTJKj2ieW5-kHEFJCEKjbcHK9bOj8X_Wvrk_Me-AQSEMgwhk9DldBD9hGKhyK0Q5DLxeJ5b5_IEd865ufgN5Ojdq7mUVGvI9TA7BjsyiPTyEkLmf1TLLP6GjZSWo-F_NHvPvtwKgZXuAL8hWG3kI3WVyjUuBWKZ_ro2ZVJUgbnf1X3pj8mpyQvtX9oMdonW7OZEg_8w'

ufirestore.set_project_id("Rn5Notifications")
ufirestore.set_access_token(access_token.decode())
raw_doc = ufirestore.get("hotbox/running")
doc = FirebaseJson.from_raw(raw_doc)
print(doc)

while True:
    wifi.check()
    sensor.measure()

    if not relay.is_on:
        sleep_ms(1000)
        relay.on()

    relay.check()

    sleep_ms(100)
