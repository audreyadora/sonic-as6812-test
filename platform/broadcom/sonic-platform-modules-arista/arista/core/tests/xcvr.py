from ...core.port import PortLayout
from ...descs.xcvr import Osfp, Qsfp28, Rj45, Sfp
from ...tests.testing import unittest

from ..fixed import FixedSystem
from ..utils import incrange
from ..xcvr import (
   OsfpSlot,
   QsfpSlot,
   SfpSlot,
   EthernetSlot,
)

from .mockinv import (
   MockGpio,
   MockInterrupt,
   MockLed,
   MockReset,
)

class MockOsfpSlot(OsfpSlot):
   pass

class MockQsfpSlot(QsfpSlot):
   pass

class MockSfpSlot(SfpSlot):
   pass

class MockEthernetSlot(EthernetSlot):
   pass

class MockFixedSystem(FixedSystem):
   def __init__(self, portLayout):
      super().__init__()
      self.portLayout = portLayout
      self.ethernetSlots = []
      self.sfpSlots = []
      self.qsfpSlots = []
      self.osfpSlots = []
      self.addrFunc = lambda addr : addr

      for p in portLayout.getEthernets():
         self.ethernetSlots.append(
            self.newComponent(
               MockEthernetSlot,
               slotId=p.index,
               leds=[MockLed()],
            )
         )

      for p in portLayout.getSfps():
         self.sfpSlots.append(
            self.newComponent(
               MockSfpSlot,
               slotId=p.index,
               addrFunc=self.addrFunc,
               interrupt=MockInterrupt(),
               presentGpio=MockGpio(),
               leds=[MockLed()],
               rxLosGpio=MockGpio(),
               txDisableGpio=MockGpio(),
               txFaultGpio=MockGpio()
            )
         )

      for p in portLayout.getQsfps():
         self.qsfpSlots.append(
            self.newComponent(
               MockQsfpSlot,
               slotId=p.index,
               addrFunc=self.addrFunc,
               presentGpio=MockGpio(),
               leds=[MockLed()],
               lpMode=MockGpio(),
               modSel=MockGpio(),
               reset=MockReset(),
            )
         )

      for p in portLayout.getOsfps():
         self.osfpSlots.append(
            self.newComponent(
               MockOsfpSlot,
               slotId=p.index,
               addrFunc=self.addrFunc,
               presentGpio=MockGpio(),
               leds=[MockLed()],
               lpMode=MockGpio(),
               modSel=MockGpio(),
               reset=MockReset(),
            )
         )

class MockXcvrTest(unittest.TestCase):
   def _checkSystem(self, system):
      self.assertEqual(len(system.getInventory().getEthernetSlots()),
                       len(system.portLayout.getEthernets()))
      self.assertEqual(len(system.getInventory().getSfpSlots()),
                       len(system.portLayout.getSfps()))
      self.assertEqual(len(system.getInventory().getQsfpSlots()),
                       len(system.portLayout.getQsfps()))
      self.assertEqual(len(system.getInventory().getOsfpSlots()),
                       len(system.portLayout.getOsfps()))
      self.assertEqual(len(system.getInventory().getXcvrSlots()),
                       len(system.portLayout.getAllPorts()))

      for p, slot in zip(system.portLayout.getEthernets(), system.ethernetSlots):
         self.assertEqual(slot.getId(), p.index)
         self._checkEthernet(slot)
      for p, slot in zip(system.portLayout.getSfps(), system.sfpSlots):
         self.assertEqual(slot.getId(), p.index)
         self._checkSfp(slot)
      for p, slot in zip(system.portLayout.getQsfps(), system.qsfpSlots):
         self.assertEqual(slot.getId(), p.index)
         self._checkQsfp(slot)
      for p, slot in zip(system.portLayout.getOsfps(), system.osfpSlots):
         self.assertEqual(slot.getId(), p.index)
         self._checkOsfp(slot)

   def _checkEthernet(self, ethernetSlot):
      self.assertIsNotNone(ethernetSlot.getXcvr())

   def _checkSfp(self, sfpSlot):
      self.assertIsNotNone(sfpSlot.getXcvr())

   def _checkQsfp(self, qsfpSlot):
      self.assertIsNotNone(qsfpSlot.getXcvr())

   def _checkOsfp(self, osfpSlot):
      self.assertIsNotNone(osfpSlot.getXcvr())

   def testXcvr(self):
      system = MockFixedSystem(
         PortLayout(
            (Rj45(i) for i in incrange(1, 8)),
            (Sfp(i) for i in incrange(9, 16)),
            (Qsfp28(i) for i in incrange(17, 24)),
            (Osfp(i) for i in incrange(25, 32)),
         )
      )
      self._checkSystem(system)

if __name__ == '__main__':
   unittest.main()
