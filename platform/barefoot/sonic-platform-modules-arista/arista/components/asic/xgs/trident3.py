
from ....core.quirk import Quirk
from ....core.register import RegisterMap, Register, RegBitRange

from ....libs.wait import waitFor

from ...vrm import VrmDetector

from . import XgsSwitchChip

class Trident3(XgsSwitchChip):
   pass

class Trident3X2RegMap(RegisterMap):
   DMU_PCU_OTP_CONFIG_9 = Register(0x6c,
      RegBitRange(21, 24, name='avsValue'),
      name='configReg',
   )

class Trident3X2(Trident3):
   REGISTER_CLS = Trident3X2RegMap

   class AvsQuirk(Quirk):

      DELAYED = True

      ASIC_TO_MILLIVOLT = {
         0x1: 800,
         0x2: 825,
         0x4: 850,
         0x8: 875,
      }

      def __init__(self, vrm):
         self.vrm_ = vrm

      @property
      def vrm(self):
         if isinstance(self.vrm_, VrmDetector):
             return self.vrm_.vrm
         return self.vrm

      def waitAsicRegisterReady(self, asic):
         waitFor(
            lambda: asic.driver.regs.configReg() != 0xffffffff,
            description='Asic config register ready',
         )

      def run(self, component):
         self.waitAsicRegisterReady(component)
         value = component.driver.regs.avsValue()
         vout = self.ASIC_TO_MILLIVOLT.get(value)
         if vout is not None:
            self.vrm.setVoutValue(vout)
