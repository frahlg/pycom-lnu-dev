# Rename this file to device_keys.py
# Put the EUI and KEY accordingly, with the device from TTN panel. Below are just examples.
# Make sure that the config.py is in .gitignore

# config.py
import ubinascii

app_eui = ubinascii.unhexlify('ADA4DAE3AC12676B')
app_key = ubinascii.unhexlify('11B0282A189B75B0B4D2D8C7FA38548B')
