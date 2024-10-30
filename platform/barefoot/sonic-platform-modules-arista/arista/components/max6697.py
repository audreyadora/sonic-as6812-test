
from ..core.component import Priority
from ..core.component.i2c import I2cComponent

from ..drivers.max6697 import Max6697KernelDriver

class Max6697(I2cComponent):
   DRIVER = Max6697KernelDriver
   PRIORITY = Priority.THERMAL
