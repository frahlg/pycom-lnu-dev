# Rename this file to device_keys.py
# Put the EUI and KEY accordingly, with the device from TTN panel. Below are just examples.
# Make sure that the config.py is in .gitignore

# config.py
import ubinascii

app_eui = ubinascii.unhexlify('XXXXXXXXXXX')
app_key = ubinascii.unhexlify('XXXXXXXXXXXXXXXXXXXXXX')
