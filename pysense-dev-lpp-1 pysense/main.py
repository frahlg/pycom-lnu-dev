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

lpp = cayenneLPP.CayenneLPP(size = 100, sock = s)

while True:
    lpp.add_temperature(mp.temperature())
    lpp.add_barometric_pressure(mpp.pressure()/100)
    lpp.add_relative_humidity(si.humidity())
    mp.altitude()
    si.dew_point()
    lpp.add_accelerometer(li.acceleration()[0],li.acceleration()[1],li.acceleration()[2])
    lpp.add_luminosity(lt.light()[0],channel=20)
    lpp.add_luminosity(lt.light()[1],channel=21)
    lpp.send()
    print('Sent LPP')
    time.sleep(30)





# while True:
#
#     press_str = '{"pressure":' + str(mpp.pressure()) +'}'
#     print(press_str)
#     send(press_str)
#
#     print("Temperature: " + str(si.temperature())+ " deg C and Relative Humidity: " + str(si.humidity()) + " %RH")
#
#     temp_str = '{"temp":' + str(si.temperature()) +'}'
#     print(temp_str)
#     send(temp_str)
#
#     RF_str = '{"RF":' + str(si.humidity()) +'}'
#     print(RF_str)
#     send(RF_str)
#
#
#
#     # convert ascii to hex values and send over LoRaWAN
# #    send(bytearray(uplink))
#     time.sleep(20)  # repeat every minute
