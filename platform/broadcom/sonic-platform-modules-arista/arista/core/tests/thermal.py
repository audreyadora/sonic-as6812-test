from __future__ import absolute_import, division, print_function

from ...tests.testing import unittest

from .. import thermal_control
from ...descs.sensor import SensorDesc, Position

class MockInvTemp(object):
   def __init__(self, desc):
      self.desc = desc

   def getDesc(self):
      return self.desc

class MockSensor(object):
   def __init__(self, presence, temp, target, overheat, critical):
      self.desc = SensorDesc(diode=0, name="N/A", position=Position.OTHER,
                             target=target, overheat=overheat, critical=critical)
      self.inv = MockInvTemp(self.desc)
      self.presence = presence
      self.temp = temp

   def get_presence(self):
      return self.presence

   def get_status(self):
      return self.get_presence()

   def get_temperature(self):
      return self.temp

   def get_inventory_object(self):
      return self.inv

class ThermalControlTest(unittest.TestCase):
   def setUp(self):
      self.thermal_control = thermal_control

   def testNormalTemp(self):
      sensor1 = MockSensor(True, 50, 40, 80, 90)
      sensor2 = MockSensor(True, 30, 20, 70, 80)
      self.assertEqual(self.thermal_control.sensorsToFanSpeed([sensor1, sensor2]),
                       self.thermal_control.MIN_FAN_SPEED)

   def testHighTemp(self):
      sensor1 = MockSensor(True, 70, 40, 80, 90)
      sensor2 = MockSensor(True, 50, 20, 70, 80)
      self.assertEqual(self.thermal_control.sensorsToFanSpeed([sensor1, sensor2]),
                       (self.thermal_control.MIN_FAN_SPEED +
                        self.thermal_control.MAX_FAN_SPEED) / 2)

   def testOneHighTemp(self):
      sensor1 = MockSensor(True, 70, 40, 80, 90)
      sensor2 = MockSensor(True, 30, 20, 70, 80)
      self.assertEqual(self.thermal_control.sensorsToFanSpeed([sensor1, sensor2]),
                       (self.thermal_control.MIN_FAN_SPEED +
                        self.thermal_control.MAX_FAN_SPEED) / 2)

   def testOverheatTemp(self):
      sensor1 = MockSensor(True, 80, 40, 80, 90)
      sensor2 = MockSensor(True, 70, 20, 70, 80)
      self.assertEqual(self.thermal_control.sensorsToFanSpeed([sensor1, sensor2]),
                       self.thermal_control.MAX_FAN_SPEED)

   def testOneOverheatTemp(self):
      sensor1 = MockSensor(True, 50, 40, 80, 90)
      sensor2 = MockSensor(True, 70, 20, 70, 80)
      self.assertEqual(self.thermal_control.sensorsToFanSpeed([sensor1, sensor2]),
                       self.thermal_control.MAX_FAN_SPEED)

   def testOneCriticalTemp(self):
      sensor1 = MockSensor(True, 50, 40, 80, 90)
      sensor2 = MockSensor(True, 80, 20, 70, 80)
      self.assertEqual(self.thermal_control.sensorsToFanSpeed([sensor1, sensor2]),
                       self.thermal_control.MAX_FAN_SPEED)

   def testOneInvalidTemp(self):
      sensor1 = MockSensor(True, 0, 0, 0, 0)
      sensor2 = MockSensor(True, 30, 20, 70, 80)
      self.assertEqual(self.thermal_control.sensorsToFanSpeed([sensor1, sensor2]),
                       self.thermal_control.MIN_FAN_SPEED)
      sensor1 = MockSensor(True, 0, 0, 0, 0)
      sensor2 = MockSensor(True, 70, 20, 70, 80)
      self.assertEqual(self.thermal_control.sensorsToFanSpeed([sensor1, sensor2]),
                       self.thermal_control.MAX_FAN_SPEED)
      sensor1 = MockSensor(True, 50, 40, 80, 90)
      sensor2 = MockSensor(True, -256, 20, 70, 80)
      self.assertEqual(self.thermal_control.sensorsToFanSpeed([sensor1, sensor2]),
                       self.thermal_control.MIN_FAN_SPEED)

if __name__ == '__main__':
   unittest.main()
