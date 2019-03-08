# Runtime at boot

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

# create an OTAA authentication parameters
#app_eui = ubinascii.unhexlify('ADA4DAE3AC12676B')
#app_key = ubinascii.unhexlify('11B0282A189B75B0B4D2D8C7FA38548B')

import config

# join a network using OTAA (Over the Air Activation)
lora.join(activation=LoRa.OTAA, auth=(config.app_eui, config.app_key), timeout=0)

# wait until the module has joined the network
while not lora.has_joined():
    time.sleep(2.5)
    print('Not yet joined...')

# create a LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

# set the LoRaWAN data rate
s.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)


print('')
