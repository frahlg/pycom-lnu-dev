import socket
import time
import binascii



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

lpp.add_temperature(mpp.temperature())
lpp.send()





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
