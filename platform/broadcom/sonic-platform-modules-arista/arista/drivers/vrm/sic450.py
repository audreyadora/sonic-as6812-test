
from . import VrmI2cUserDriver

class Sic450UserDriver(VrmI2cUserDriver):
   IDENTIFY_SEQUENCE = [
      (0xad, 0x0002),
   ]
