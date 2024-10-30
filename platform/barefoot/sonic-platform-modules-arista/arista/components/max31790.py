
from ..core.component import Priority
from ..core.component.i2c import I2cComponent

from ..drivers.max31790 import Max31790KernelDriver

class Max31790(I2cComponent):
   PRIORITY = Priority.THERMAL
   DRIVER = Max31790KernelDriver
