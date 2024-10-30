
from ..hwapi import HwApi
from ...tests.testing import unittest

class HwApiTest(unittest.TestCase):
   def testEqual(self):
      self.assertEqual(HwApi(2), HwApi(2))
      self.assertEqual(HwApi(2), HwApi(2, 0))
      self.assertEqual(HwApi(2, 0), HwApi(2))

   def testGreater(self):
      self.assertGreater(HwApi(3), HwApi(2))
      self.assertGreater(HwApi(3), HwApi(2, 1))
      self.assertGreater(HwApi(3, 1), HwApi(3, 0))
      self.assertGreater(HwApi(3, 1), HwApi(3))

   def testLess(self):
      self.assertLess(HwApi(2), HwApi(3))
      self.assertLess(HwApi(2, 1), HwApi(3))
      self.assertLess(HwApi(2, 0), HwApi(2, 1))
      self.assertLess(HwApi(2), HwApi(2, 1))

   def testGreaterEqual(self):
      self.assertGreaterEqual(HwApi(2), HwApi(2))
      self.assertGreaterEqual(HwApi(2), HwApi(2, 0))
      self.assertGreaterEqual(HwApi(3), HwApi(2))
      self.assertGreaterEqual(HwApi(3), HwApi(2, 1))
      self.assertGreaterEqual(HwApi(2, 1), HwApi(2, 1))

   def testLessEqual(self):
      self.assertLessEqual(HwApi(2), HwApi(2))
      self.assertLessEqual(HwApi(2, 0), HwApi(2))
      self.assertLessEqual(HwApi(2), HwApi(3))
      self.assertLessEqual(HwApi(2, 1), HwApi(3))
      self.assertLessEqual(HwApi(2, 1), HwApi(2, 1))

if __name__ == '__main__':
   unittest.main()
