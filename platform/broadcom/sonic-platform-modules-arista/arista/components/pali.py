from ..components.lm75 import Tmp75

from ..core.component.i2c import I2cComponent
from ..core.component import Priority
from ..core.fan import FanSlot
from ..core.utils import incrange

from ..descs.fan import FanDesc, FanPosition
from ..descs.led import LedDesc, LedColor
from ..descs.sensor import Position, SensorDesc

from ..drivers.pali import Pali2FanCpldKernelDriver

from .eeprom import At24C32

class Pali2FanCpld(I2cComponent):
   DRIVER = Pali2FanCpldKernelDriver
   PRIORITY = Priority.COOLING

class Pali2:

   FAN_COUNT = 4

   def __init__(self, parent, bus):
      parent.newComponent(Tmp75, addr=bus.i2cAddr(0x48), sensors=[
         SensorDesc(diode=0, name='Outlet', position=Position.OUTLET,
            target=65, overheat=80, critical=95),
      ])

      self.eeprom = parent.newComponent(At24C32, addr=bus.i2cAddr(0x50))

      self.cpld = parent.newComponent(Pali2FanCpld, addr=bus.i2cAddr(0x60))

      for slotId in incrange(1, self.FAN_COUNT):
         fan = self.cpld.addFan(FanDesc(fanId=slotId, position=FanPosition.INLET))
         led = self.cpld.addFanLed(LedDesc(name='fan%d' % slotId,
            colors=[LedColor.RED, LedColor.GREEN, LedColor.OFF]))
         parent.newComponent(FanSlot, slotId=slotId, led=led, fans=[fan])
