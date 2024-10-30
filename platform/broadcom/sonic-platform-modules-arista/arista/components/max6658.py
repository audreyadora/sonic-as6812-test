
from ..core.component import Priority
from ..core.component.i2c import I2cComponent

from ..drivers.max6658 import Max6658KernelDriver

class Max6658(I2cComponent):
   DRIVER = Max6658KernelDriver
   PRIORITY = Priority.THERMAL
