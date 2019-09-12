import time
import ubinascii
from machine import Pin
from onewire import DS18X20
from onewire import OneWire

#DS18B20 data line connected to pin P10
ow = OneWire(Pin('P10'))
temp = DS18X20(ow)

while True:

    temp.start_conversion()
    time.sleep(1)
    t_ = temp.read_temp_async()
    time.sleep(1)
    print("DS18b20 temperature: " + str(t_))
    time.sleep(5)
