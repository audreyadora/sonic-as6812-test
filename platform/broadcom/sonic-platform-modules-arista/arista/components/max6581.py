
from ..core.component import Priority
from ..core.component.i2c import I2cComponent

from ..drivers.max6581 import Max6581KernelDriver

class Max6581(I2cComponent):
   DRIVER = Max6581KernelDriver
   PRIORITY = Priority.THERMAL
