
from ...core.component import Priority
from ...core.component.i2c import I2cComponent
from ...core.register import Register, RegBitField

from ...drivers.rook import (
   LaFanCpldKernelDriver,
   TehamaFanCpldKernelDriver,
   RookStatusLedKernelDriver,
)

from ..cpld import SysCpld, SysCpldCommonRegistersV2

class RookCpldRegisters(SysCpldCommonRegistersV2):
   pass

class RookSysCpld(SysCpld):
   REGISTER_CLS = RookCpldRegisters

class RookStatusLeds(I2cComponent):
   DRIVER = RookStatusLedKernelDriver
   PRIORITY = Priority.LED

class RookFanCpld(I2cComponent):
   PRIORITY = Priority.COOLING
   FAN_COUNT = 0

class LaFanCpld(RookFanCpld):
   DRIVER = LaFanCpldKernelDriver
   FAN_COUNT = 4

class TehamaFanCpld(RookFanCpld):
   DRIVER = TehamaFanCpldKernelDriver
   FAN_COUNT = 5
