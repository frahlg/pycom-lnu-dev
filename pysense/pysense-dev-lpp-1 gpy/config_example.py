# Rename this file to device_keys.py
# Put the EUI and KEY accordingly, with the device from TTN panel. Below are just examples.
# Make sure that the config.py is in .gitignore

# config.py
import ubinascii

app_eui = ubinascii.unhexlify('XXXXDAE3AC12XXXX')
app_key = ubinascii.unhexlify('XXXX282A189B75B0B4D2D8C7FA38XXXX')
