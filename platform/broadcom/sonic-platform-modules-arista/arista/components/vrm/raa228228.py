
from ...core.component.i2c import I2cComponent
from ...core.driver.user.i2c import I2cDevDriver
from ...core.log import getLogger
from ...core.quirk import Quirk

logging = getLogger(__name__)

class Raa228228GainQuirk(Quirk):
   def __init__(self, description=None, model=None, gain=None):
      self.description = description
      self.model = model
      self.gain = gain

   def __str__(self):
      return self.description or f'{self.__class__.__name__}'

   def run(self, component):
      model = component.driver.read_block_data(0x9a)
      if model != self.model:
         return
      component.driver.write_byte_data(0x00, 0x00)
      component.driver.write_bytes([0xde] + self.gain)
      if component.driver.read_bytes([0xde], 4) != self.gain:
         logging.error("Failed to apply %s", self.description)

class Raa228228(I2cComponent):
   DRIVER = I2cDevDriver

   def setup(self):
      self.applyQuirks()
