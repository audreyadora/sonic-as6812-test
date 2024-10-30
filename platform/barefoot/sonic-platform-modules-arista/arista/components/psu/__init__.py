from ...core.component import Priority
from ...core.component.i2c import I2cComponent

from ...drivers.pmbus import PmbusKernelDriver

class PmbusPsu(I2cComponent):
   DRIVER = PmbusKernelDriver
   PRIORITY = Priority.POWER
