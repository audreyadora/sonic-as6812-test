from ..core.platform import registerPlatform
from ..core.port import PortLayout
from ..core.utils import incrange

from ..components.psu.delta import DPS495CB, DPS750AB
from ..components.lm73 import Lm73

from ..descs.sensor import Position, SensorDesc
from ..descs.xcvr import Qsfp28, Sfp

from .alhambra import Alhambra

@registerPlatform()
class Mineral(Alhambra):

   SID = ['Mineral', 'MineralSsd']
   SKU = ['DCS-7170-32C', 'DCS-7170-32C-M']

   PORTS = PortLayout(
      (Qsfp28(i, leds=4) for i in incrange(1, 32)),
      (Sfp(i) for i in incrange(33, 34)),
   )

   def __init__(self):
      super(Mineral, self).__init__(hasLmSensor=False, hasCpuLeds=False, psus=[
         DPS495CB,
         DPS750AB,
      ])
      self.scd.newComponent(Lm73, self.scd.i2cAddr(7, 0x4a), sensors=[
         SensorDesc(diode=0, name='Front-panel temp sensor',
                    position=Position.OTHER, target=55, overheat=75, critical=85),
      ])

@registerPlatform()
class MineralD(Mineral):

   SID = ['MineralD']
   SKU = ['DCS-7170-32CD']
