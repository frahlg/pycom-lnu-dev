import socket
import time
import binascii

from pysense import Pysense
from LIS2HH12 import LIS2HH12
from SI7006A20 import SI7006A20
from LTR329ALS01 import LTR329ALS01
from MPL3115A2 import MPL3115A2,ALTITUDE,PRESSURE

py = Pysense()
mp = MPL3115A2(py,mode=ALTITUDE) # Returns height in meters. Mode may also be set to PRESSURE, returning a value in Pascals
si = SI7006A20(py)
lt = LTR329ALS01(py)
li = LIS2HH12(py)

# Pysense specific


print("MPL3115A2 temperature: " + str(mp.temperature()))
print("Altitude: " + str(mp.altitude()))
mpp = MPL3115A2(py,mode=PRESSURE) # Returns pressure in Pa. Mode may also be set to ALTITUDE, returning a value in meters
print("Pressure: " + str(mpp.pressure()))

print("Temperature: " + str(si.temperature())+ " deg C and Relative Humidity: " + str(si.humidity()) + " %RH")
print("Dew point: "+ str(si.dew_point()) + " deg C")
t_ambient = 24.4
print("Humidity Ambient for " + str(t_ambient) + " deg C is " + str(si.humid_ambient(t_ambient)) + "%RH")

print("Light (channel Blue lux, channel Red lux): " + str(lt.light()))

print("Acceleration: " + str(li.acceleration()))
print("Roll: " + str(li.roll()))
print("Pitch: " + str(li.pitch()))

print("Battery voltage: " + str(py.read_battery_voltage()))
###





from network import LoRa
import config

# initialize LORAWAN mode for EU region
lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)

# print DevEUI of the device, use this when provisioning it in your network server
print("DevEUI: " + binascii.hexlify(lora.mac()).decode('utf-8').upper())

# OTAA authentication parameters, replace these with your own

print("Joining network using OTAA (Over the Air Activation)")
lora.join(activation=LoRa.OTAA, auth=(config.app_eui, config.app_key), timeout=0)

# wait until the module has joined the network
while not lora.has_joined():
    time.sleep(2.5)
    print('Not yet joined...')

print("Joined network")

# create socket to be used for LoRa communication
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

# configure data rate
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)

# make the socket blocking
# (waits for the data to be sent and for the 2 receive windows to expire)
s.setblocking(True)

import cayenneLPP
lpp = cayenneLPP.CayenneLPP(size = 200, sock = s)




lpp.add_temperature(mp.temperature())
lpp.add_pressure(mpp.pressure())

lpp.send()
