from network import LoRa
import socket
import time
import ubinascii


import machine
import math
import network
import os
import time
import utime
import gc
from machine import RTC
from machine import SD
from L76GNSS import L76GNSS
from pytrack import Pytrack

import cayenneLPP



# Initialise LoRa in LORAWAN mode.
# Please pick the region that matches where you are using the device:
# Asia = LoRa.AS923
# Australia = LoRa.AU915
# Europe = LoRa.EU868
# United States = LoRa.US915
lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)

print("DevEUI: " + ubinascii.hexlify(lora.mac()).decode('utf-8').upper())

# create an OTAA authentication parameters
app_eui = ubinascii.unhexlify('70B3D57ED0021533')
app_key = ubinascii.unhexlify('AEDA586B478A097FE1A6EC279C474AA3')
#70b3d5499f2e3d63
# join a network using OTAA (Over the Air Activation)
lora.join(activation=LoRa.OTAA, auth=(app_eui, app_key), timeout=0)

while not lora.has_joined():
    print('Not yet joined...')
    time.sleep(2)

print("Joined network")

# create socket to be used for LoRa communication
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

# configure data rate
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)

# make the socket blocking
# (waits for the data to be sent and for the 2 receive windows to expire)
s.setblocking(True)


#### Pytrack

gc.enable()

# setup rtc
# rtc = machine.RTC()
# rtc.ntp_sync("pool.ntp.org")
# utime.sleep_ms(750)
# print('\nRTC Set from NTP to UTC:', rtc.now())
# utime.timezone(7200)
# print('Adjusted from UTC to EST timezone', utime.localtime(), '\n')

py = Pytrack()
l76 = L76GNSS(py, timeout=5000)

# sd = SD()
# os.mount(sd, '/sd')
# f = open('/sd/gps-record.txt', 'w')

lpp = cayenneLPP.CayenneLPP(size = 100, sock = s)


while (True):
    coord = l76.coordinates()
    if isinstance(coord, int):
        lpp.add_gps(3, coord, 2)
    #f.write("{} - {}\n".format(coord, rtc.now()))
    print(coord)
    lpp.send(reset_payload = True)
    time.sleep(60)
