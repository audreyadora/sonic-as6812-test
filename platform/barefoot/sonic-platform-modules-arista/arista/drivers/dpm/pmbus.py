
from ...core.log import getLogger

from ...core.driver.user.i2c import I2cDevDriver

logging = getLogger(__name__)

SMBUS_BLOCK_MAX_SZ = 32

class PmbusUserDriver(I2cDevDriver):
   def __init__(self, addr=None, registers=None, **kwargs):
      super(PmbusUserDriver, self).__init__(addr=addr, **kwargs)
      self.registers = registers

   def getBlock(self, reg):
      size = self.read_byte_data(reg) + 1
      data = self.read_bytes([reg], size)
      return data[1:data[0]+1]

   def setBlock(self, reg, data):
      self.write_bytes([reg, len(data)] + data)
