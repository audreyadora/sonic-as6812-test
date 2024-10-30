
from ...core.platform import registerPlatform
from ...core.utils import incrange

from ..cpu.hedgehog import HedgehogCpu

from ...components.denali.linecard import StandbyScdRegisterMap
from ...components.eeprom import At24C512
from ...components.lm75 import Tmp75
from ...components.phy.b52 import B52
from ...components.plx import PlxPortDesc
from ...components.scd import I2cScd
from ...components.tmp464 import Tmp464

from ...descs.sensor import Position, SensorDesc

from .clearwater import ClearwaterBase

class ClearwaterScdRegMap(StandbyScdRegisterMap):
   pass

class ClearwaterCpuBase(ClearwaterBase):
   CPU_CLS = HedgehogCpu
   STANDBY_TEMP_SENSORS_CLS = Tmp75

   def mainDomain(self):
      super(ClearwaterCpuBase, self).mainDomain()

      self.scd.newComponent(Tmp464, self.scd.i2cAddr(8, 0x48), sensors=[
         SensorDesc(diode=0, name='Center back', position=Position.OTHER,
                    target=75, overheat=85, critical=95),
         SensorDesc(diode=1, name='Fap0 core0', position=Position.OTHER,
                    target=85, overheat=100, critical=105),
         SensorDesc(diode=2, name='Fap0 core1', position=Position.OTHER,
                    target=85, overheat=100, critical=105),
         SensorDesc(diode=3, name='PCIE', position=Position.OTHER,
                    target=75, overheat=85, critical=90),
      ])

      # Riser cards prefdl
      for riserId in incrange(1, 12):
         bus = 95 + riserId
         self.scd.newComponent(At24C512, addr=self.scd.i2cAddr(bus, 0x50),
                               label='card%d_riser%s' % (self.slot.slotId, riserId))

   def standbyDomain(self):
      super(ClearwaterCpuBase, self).standbyDomain()
      self.syscpld = self.pca.newComponent(I2cScd, addr=self.pca.i2cAddr(0x23),
                                           registerCls=ClearwaterScdRegMap)

   def controlDomain(self):
      super(ClearwaterCpuBase, self).controlDomain()
      assert self.control, "Control plane power domain not initialized"
      self.CPU_CLS.addCpuDpm(bus=self.control, addr=self.pca.i2cAddr(0x4f))

@registerPlatform()
class Clearwater2(ClearwaterCpuBase):
   SID = ['Clearwater2']
   SKU = ['7800R3-48CQ2-LC', '7800R-48QC2-LC']

   MAX_POWER_DRAW = 622
   TYP_POWER_DRAW = 474

   PLX_PORTS = [
      PlxPortDesc(port=0, name='sup1', upstream=True),
      PlxPortDesc(port=1, name='lcpu', vs=PlxPortDesc.VS1, upstream=True),
      PlxPortDesc(port=2, name='sup2', upstream=True),
      PlxPortDesc(port=3, name='je0', vs=PlxPortDesc.VS1),
      PlxPortDesc(port=5, name='scd', vs=PlxPortDesc.VS1),
      PlxPortDesc(port=13, name='gmac'),
   ]

   XCVR_BUS_OFFSET = 24

@registerPlatform()
class Clearwater2Ms(Clearwater2):
   SID = ['Clearwater2Ms']
   SKU = ['7800R3-48CQM2-LC', '7800R-48QCM2-LC']

   MAX_POWER_DRAW = 696
   TYP_POWER_DRAW = 511

   PHY_CLS = B52
