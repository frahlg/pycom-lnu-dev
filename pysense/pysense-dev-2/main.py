# See https://docs.pycom.io for more information regarding library specifics

from pysense import Pysense
from LIS2HH12 import LIS2HH12
from SI7006A20 import SI7006A20
from LTR329ALS01 import LTR329ALS01
from MPL3115A2 import MPL3115A2,ALTITUDE,PRESSURE

from network import LoRa
import socket
import time
import binascii
import config
import ustruct



py = Pysense()
mp = MPL3115A2(py,mode=ALTITUDE) # Returns height in meters. Mode may also be set to PRESSURE, returning a value in Pascals
si = SI7006A20(py)
lt = LTR329ALS01(py)
li = LIS2HH12(py)




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


### Push data to TTN



#####


"""
    OTAA Node example  as per LoRaWAN EU868 regional specification
    - compatible with the LoPy Nano Gateway and all other LoraWAN gateways
    - tested works with a LoRaServer and TTN servers
"""

from network import LoRa
import socket
import binascii
import struct
import time

LORA_CHANNEL = 0 # zero = random
LORA_NODE_DR = 4
'''
    utility function to setup the lora channels
'''
def prepare_channels(lora, channel, data_rate):
    EU868_FREQUENCIES = [
        { "chan": 1, "fq": "868100000" },
        { "chan": 2, "fq": "868300000" },
        { "chan": 3, "fq": "868500000" },
        { "chan": 4, "fq": "867100000" },
        { "chan": 5, "fq": "867300000" },
        { "chan": 6, "fq": "867500000" },
        { "chan": 7, "fq": "867700000" },
        { "chan": 8, "fq": "867900000" },
    ]
    if not channel in range(0, 9):
        raise RuntimeError("channels should be in 0-8 for EU868")

    if channel == 0:
        import  uos
        channel = (struct.unpack('B',uos.urandom(1))[0] % 7) + 1

    upstream = (item for item in EU868_FREQUENCIES if item["chan"] == channel).__next__()

    # set the 3 default channels to the same frequency
    lora.add_channel(0, frequency=int(upstream.get('fq')), dr_min=0, dr_max=5)
    lora.add_channel(1, frequency=int(upstream.get('fq')), dr_min=0, dr_max=5)
    lora.add_channel(2, frequency=int(upstream.get('fq')), dr_min=0, dr_max=5)

    for i in range(3, 16):
        lora.remove_channel(i)

    return lora

'''
    call back for handling RX packets
'''
def lora_cb(lora):
    events = lora.events()
    if events & LoRa.RX_PACKET_EVENT:
        if lora_socket is not None:
            frame, port = lora_socket.recvfrom(512) # longuest frame is +-220
            print(port, frame)
    if events & LoRa.TX_PACKET_EVENT:
        print("tx_time_on_air: {} ms @dr {}", lora.stats().tx_time_on_air, lora.stats().sftx)


'''
    Main operations: this is sample code for LoRaWAN on EU868
'''

lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868, device_class=LoRa.CLASS_C)


# create an OTA authentication params
dev_eui = config.app_eui
app_key = config.app_key # not used leave empty loraserver.io
#nwk_key = binascii.unhexlify('a926e5bb85271f2da0440f2f4200afe3')

prepare_channels(lora, 1, LORA_NODE_DR)

# join a network using OTAA
lora.join(activation=LoRa.OTAA, auth=(dev_eui, app_key), timeout=0,  dr=LORA_NODE_DR) # DR is 2 in v1.1rb but 0 worked for ne

# wait until the module has joined the network
print('Over the air network activation ... ', end='')
while not lora.has_joined():
    time.sleep(2.5)
    print('.', end='')
print('')

# create a LoRa socket
lora_socket = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

# set the LoRaWAN data rate
lora_socket.setsockopt(socket.SOL_LORA, socket.SO_DR, LORA_NODE_DR)

# msg are confirmed at the FMS level
lora_socket.setsockopt(socket.SOL_LORA, socket.SO_CONFIRMED, 0)

# make the socket non blocking y default
lora_socket.setblocking(False)

lora.callback(trigger=( LoRa.RX_PACKET_EVENT |
                        LoRa.TX_PACKET_EVENT |
                        LoRa.TX_FAILED_EVENT  ), handler=lora_cb)

time.sleep(4) # this timer is important and caused me some trouble ...
