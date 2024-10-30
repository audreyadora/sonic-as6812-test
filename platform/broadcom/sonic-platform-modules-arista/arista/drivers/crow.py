
from ..core.driver.kernel.i2c import I2cKernelDriver

class CrowFanCpldKernelDriver(I2cKernelDriver):
   MODULE = 'crow-fan-driver'
   NAME = 'crow_cpld'
