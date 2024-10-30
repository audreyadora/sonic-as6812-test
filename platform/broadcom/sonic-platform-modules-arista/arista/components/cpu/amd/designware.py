
from ....core.types import I2cBus

class DesignWareI2cBus(I2cBus):
   def __init__(self, bus):
      # NOTE: this i2c adapters don't have a unique naming
      #       therefore assume probe order but not contiguous kernel bus ids
      name = 'Synopsys DesignWare I2C adapter'
      super().__init__(name, idx=bus)
