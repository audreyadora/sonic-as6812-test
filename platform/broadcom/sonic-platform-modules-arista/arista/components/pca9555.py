
from ..core.component import Priority
from ..core.component.i2c import I2cComponent

from ..drivers.pca9555 import Pca9555I2cDevDriver

class Pca9555(I2cComponent):

   DRIVER = Pca9555I2cDevDriver
   PRIORITY = Priority.DEFAULT

   def resetConfig(self):
      self.driver.reset()

   def addGpio(self, name):
      return self.inventory.addGpio(self.driver.getGpio(name))

   def addGpioLed(self, name, **kwargs):
      return self.inventory.addLed(self.driver.getGpioLed(name, **kwargs))

   def addRedGreenGpioLed(self, name, rname, gname, **kwargs):
      return self.inventory.addLed(
                   self.driver.getRedGreenGpioLed(name, rname, gname, **kwargs))

   def __getattr__(self, key):
      return getattr(self.driver.regs, key)
