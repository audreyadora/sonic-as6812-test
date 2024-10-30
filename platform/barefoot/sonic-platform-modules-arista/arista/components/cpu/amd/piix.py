
from ....core.types import I2cBus

class PiixI2cBus(I2cBus):
   def __init__(self, port, addr):
      name = 'SMBus PIIX4 adapter port %d at %04x' % (port, addr)
      super().__init__(name)
