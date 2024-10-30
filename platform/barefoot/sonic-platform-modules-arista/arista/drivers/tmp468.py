
from ..core.driver.kernel.i2c import I2cKernelDriver

class Tmp468KernelDriver(I2cKernelDriver):
   MODULE = 'tmp468'
   NAME = 'tmp468'

class Tmp464KernelDriver(Tmp468KernelDriver):
   NAME = 'tmp464'
