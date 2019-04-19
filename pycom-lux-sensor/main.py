
from tsl2591 import Tsl2591

### Connect SDA to PIN 8. SDC = PIN 23.
### Can be changed in the library.

lux = Tsl2591(0)
print(lux.get_full_luminosity())

