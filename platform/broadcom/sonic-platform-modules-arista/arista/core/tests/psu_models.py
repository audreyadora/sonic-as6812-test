
from ..log import getLogger
from ..psu import PsuIdent, getPsuManager

from ...descs.psu import PsuDesc

from ...tests.testing import unittest

logging = getLogger(__name__)

class PsuModelTest(unittest.TestCase):

   def assertValidI2cAddr(self, addr):
      self.assertGreater(addr, 3)
      self.assertLess(addr, 120)

   def _testPsuModel(self, model):
      if not model.IDENTIFIERS:
         logging.info('Skipping power supply base model %s' % model)
         return
      logging.info('Testing power supply model %s' % model)
      self.assertIsNotNone(model.MANUFACTURER)
      self.assertIsNotNone(model.IDENTIFIERS)
      identifiers = set()
      for ident in model.IDENTIFIERS:
         self.assertIsInstance(ident, PsuIdent)
         identifiers.add(ident.partName)
      self.assertEqual(len(identifiers), len(model.IDENTIFIERS))
      self.assertValidI2cAddr(model.IPMI_ADDR)
      if model.PMBUS_ADDR:
         # Fixed non-SMBus-accessible PSUs don't have this
         self.assertValidI2cAddr(model.PMBUS_ADDR)
      if model.PMBUS_CLS:
         # Fixed non-SMBus-accessible PSUs don't have this
         self.assertIsInstance(model.PMBUS_CLS, object)
      self.assertGreater(model.CAPACITY, 0)
      self.assertIsInstance(model.DUAL_INPUT, bool)
      if model.DRIVER is not None:
         self.assertIsInstance(model.DRIVER, str)
      self.assertIsInstance(model.DESCRIPTION, PsuDesc)

   def testPsuModels(self):
      models = getPsuManager().psuModels
      self.assertTrue(models)
      for model in models:
         self._testPsuModel(model)

if __name__ == '__main__':
   unittest.main()
