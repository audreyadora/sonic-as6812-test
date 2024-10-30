
from ..core.component import Priority
from ..core.component.i2c import I2cComponent

from ..drivers.tmp468 import Tmp468KernelDriver

class Tmp468(I2cComponent):
   DRIVER = Tmp468KernelDriver
   PRIORITY = Priority.THERMAL
