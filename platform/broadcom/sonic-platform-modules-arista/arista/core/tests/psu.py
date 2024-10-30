
from ...tests.testing import unittest, patch

from ...descs.fan import FanDesc, FanPosition
from ...descs.psu import PsuDesc
from ...descs.rail import RailDesc, RailDirection
from ...descs.sensor import Position, SensorDesc

from ..component import Component, Priority
from ..cooling import Airflow
from ..fixed import FixedSystem
from ..psu import PsuSlot, PsuModel, PsuIdent
from ..utils import incrange

from .mockinv import (
   MockGpio,
   MockLed,
)

class MockPmbus(Component):
   def addTempSensors(self, sensors):
      pass
   def addFans(self, fans):
      pass
   def addRails(self, rails):
      pass

class MockPsuModel(PsuModel):
   PMBUS_CLS = MockPmbus

class PsuVendor1(MockPsuModel):
   MANUFACTURER = 'VENDOR1'
   PMBUS_ADDR = 0x58
   DESCRIPTION = PsuDesc(
      sensors=[
         SensorDesc(diode=0, name='Power supply %(psuId)d', position=Position.OTHER,
                    target=80, overheat=95, critical=100),
      ],
      fans=[
         FanDesc(fanId=1, name='FanP%(psuId)d/%(fanId)d',
                 position=FanPosition.OUTLET),
      ],
      rails=[
         RailDesc(railId=0, direction=RailDirection.INPUT),
         RailDesc(railId=1, direction=RailDirection.OUTPUT),
         RailDesc(railId=2, direction=RailDirection.OUTPUT),
      ],
   )

class PsuModel1(PsuVendor1):
   IDENTIFIERS = [
      PsuIdent('MODEL1-0', 'SKU1-F', Airflow.EXHAUST),
      PsuIdent('MODEL1-1', 'SKU1-R', Airflow.INTAKE),
   ]

class PsuModel2(PsuVendor1):
   IDENTIFIERS = [
      PsuIdent('MODEL2-0', 'SKU2-F', Airflow.EXHAUST),
      PsuIdent('MODEL2-1', 'SKU2-R', Airflow.INTAKE),
   ]

class PsuModel3(MockPsuModel):
   MANUFACTURER = 'VENDOR2'
   PMBUS_ADDR = 0x17
   IDENTIFIERS = [
      PsuIdent('MODEL-F', 'SKU3-F', Airflow.EXHAUST),
      PsuIdent('MODEL-R', 'SKU3-R', Airflow.INTAKE),
   ]

class MockPmbusDetect(object):
   def __init__(self, mockData):
      if isinstance(mockData, int):
         mockData = { 'id': 'unknown', 'model': 'unknown' }
      self.mockData = mockData

   def id(self):
      return self.mockData['id']

   def model(self):
      return self.mockData['model']

   def getMetadata(self):
      return self.mockData

   def exists(self):
      return True

class MockPsuSlot(PsuSlot):
   pass

class MockFixedSystem(FixedSystem):
   def __init__(self, psus, numPsus=2, psuFunc=lambda x: x):
      super(MockFixedSystem, self).__init__()
      self.slots = []
      self.numPsus = numPsus
      for i in incrange(1, numPsus):
         self.slots.append(self.newComponent(
            MockPsuSlot,
            slotId=i,
            addrFunc=psuFunc,
            presentGpio=MockGpio(),
            inputOkGpio=MockGpio(),
            outputOkGpio=MockGpio(),
            led=MockLed(),
            psus=psus,
         ))

@patch('arista.core.psu.PsuPmbusDetect', MockPmbusDetect)
class TestPsu(unittest.TestCase):
   def _checkSystem(self, system):
      self.assertEqual(len(system.getInventory().getPsuSlots()), system.numPsus)
      self.assertTrue(system.components)
      system.setup(filters=Priority.backgroundFilter)
      for i, slot in enumerate(system.slots, 1):
         self.assertEqual(slot.slotId, i)

   def _checkPsu(self, system, psuId, model):
      slot = system.slots[psuId]
      self.assertIsNotNone(slot.model)
      self.assertIsInstance(slot.model, model)

   def testBasicNoPsu(self):
      system = MockFixedSystem([PsuModel1, PsuModel2])
      self._checkSystem(system)

   def testBasic1PsuPresent(self):
      system = MockFixedSystem([PsuModel1, PsuModel2])
      system.slots[0].presentGpio.value = 1
      self._checkSystem(system)

   def testBasic2PsuPresent(self):
      system = MockFixedSystem([PsuModel1, PsuModel2])
      system.slots[0].presentGpio.value = 1
      system.slots[1].presentGpio.value = 1
      self._checkSystem(system)

   def testPsuDetected(self):
      def psuFunc(_):
         return { 'id': 'VENDOR1', 'model': 'MODEL2-0' }
      system = MockFixedSystem([PsuModel1, PsuModel2], psuFunc=psuFunc)
      system.slots[0].presentGpio.value = 1
      self._checkSystem(system)
      self._checkPsu(system, 0, PsuModel2)

if __name__ == '__main__':
   unittest.main()
