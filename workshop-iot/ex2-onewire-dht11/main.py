import time
import ubinascii
from machine import Pin
import dht

dht_pin = Pin('P10', mode=Pin.OPEN_DRAIN)


while True:
    temp, hum = dht.DHT22(dht_pin)
    temp_str = '{}.{}'.format(temp//10, temp % 10)
    hum_str = '{}.{}'.format(hum//10, hum % 10)
    time.sleep(1)
    print("DHT temperature: " + temp_str)
    print("DHT RH: " + hum_str)
    time.sleep(5)
