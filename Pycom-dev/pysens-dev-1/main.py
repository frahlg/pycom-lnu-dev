from network import LoRa
import socket
import time
import ubinascii



# Initialise LoRa in LORAWAN mode.
# Please pick the region that matches where you are using the device:
# Asia = LoRa.AS923
# Australia = LoRa.AU915
# Europe = LoRa.EU868
# United States = LoRa.US915
lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)

print("DevEUI: " + ubinascii.hexlify(lora.mac()).decode('utf-8').upper())

# create an OTAA authentication parameters
app_eui = ubinascii.unhexlify('70B3D57ED0018D8B')
app_key = ubinascii.unhexlify('9C16CBBB511BD1D642A54786543FBA5C')
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


mpp = MPL3115A2(py,mode=PRESSURE) # Returns pressure in Pa. Mode may also be set to ALTITUDE, returning a value in meters
print("MPL3115A2 temperature: " + str(mp.temperature()))



import cayenneLPP

lpp = cayenneLPP.CayenneLPP(size = 100, sock = s)


#lpp.addGPS(3, 52.37365, 4.88650, 2);


while True:

    lpp.add_temperature(mp.temperature());
    lpp.add_barometric_pressure(mpp.pressure()/100);
    lpp.add_relative_humidity(si.humidity())
    lpp.add_accelerometer(li.acceleration()[0],li.acceleration()[1],li.acceleration()[2])
    lpp.add_luminosity(lt.light()[0],channel=20)
    lpp.add_luminosity(lt.light()[1],channel=21)
    lpp.add_analog_input(round(py.read_battery_voltage(),1),channel=22)
    #lpp.add_generic(116,round(py.read_battery_voltage(),1),channel=23,precision=0.1)
    print("Battery voltage: " + str(py.read_battery_voltage()))

    print("Humidity " + str(si.humidity()))
    print("Pressure hPa: " + str(mpp.pressure()/100))
    print("MPL3115A2 temperature: " + str(mp.temperature()))

    lpp.send(reset_payload = True)

    time.sleep(30)
