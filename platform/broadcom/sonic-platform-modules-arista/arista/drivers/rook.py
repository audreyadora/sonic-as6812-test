
from ..core.driver.kernel.i2c import I2cKernelDriver
from ..core.driver.kernel.sysfs import LedRgbSysfsImpl

class RookStatusLedKernelDriver(I2cKernelDriver):
   MODULE = 'rook-led-driver'
   NAME = 'rook_leds'

   def getLed(self, desc, **kwargs):
      return LedRgbSysfsImpl(self, desc, prefix=self.NAME, **kwargs)

class RookFanCpldKernelDriver(I2cKernelDriver):
   MODULE = 'rook-fan-cpld'

class LaFanCpldKernelDriver(RookFanCpldKernelDriver):
   NAME = 'la_cpld'

class TehamaFanCpldKernelDriver(RookFanCpldKernelDriver):
   NAME = 'tehama_cpld'
