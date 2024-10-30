
from . import VrmI2cUserDriver

class Tps549D22UserDriver(VrmI2cUserDriver):
   IDENTIFY_SEQUENCE = [
      (0xfc, 0x0201),
      (0xad, None),
   ]
