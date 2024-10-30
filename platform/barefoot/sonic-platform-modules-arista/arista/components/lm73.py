
from ..core.component import Priority
from ..core.component.i2c import I2cComponent

from ..drivers.lm73 import Lm73KernelDriver

class Lm73(I2cComponent):
   DRIVER = Lm73KernelDriver
   PRIORITY = Priority.THERMAL
