
from ..core.component import Priority
from ..core.component.i2c import I2cComponent

from ..drivers.lm75 import Lm75KernelDriver, Tmp75KernelDriver

class Lm75(I2cComponent):
   DRIVER = Lm75KernelDriver
   PRIORITY = Priority.THERMAL

class Tmp75(Lm75):
   DRIVER = Tmp75KernelDriver
