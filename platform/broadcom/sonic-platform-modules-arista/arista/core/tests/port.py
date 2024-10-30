from ...core.utils import incrange
from ...descs.xcvr import Osfp, Qsfp, Rj45, Sfp, Xcvr
from ...tests.testing import unittest
from ..port import PortLayout

class PortLayoutTest(unittest.TestCase):

   nEthernets = 8
   nSfps = 8
   nQsfps = 8
   nOsfps = 8

   def _checkPortLayout(self, portLayout):
      self.assertEqual(len(portLayout.getEthernets()), self.nEthernets)
      self.assertEqual(len(portLayout.getSfps()), self.nSfps)
      self.assertEqual(len(portLayout.getQsfps()), self.nQsfps)
      self.assertEqual(len(portLayout.getOsfps()), self.nOsfps)

      ports = portLayout.getAllPorts()
      for p in ports:
         self.assertIsInstance(p, Xcvr)

      families = [Rj45, Sfp, Qsfp, Osfp]
      for p in ports:
         index = ((1 if p.index >
                     self.nEthernets else 0) +
                  (1 if p.index >
                     self.nEthernets + self.nSfps else 0) +
                  (1 if p.index >
                     self.nEthernets + self.nSfps + self.nQsfps else 0))
         self.assertTrue(isinstance(p, families[index]))

      indexes = [p.index for p in ports]
      self.assertListEqual(indexes, sorted(indexes))

      self.assertEqual(len(ports), len(set(indexes)))
      self.assertEqual(1, min(indexes))
      self.assertEqual(len(ports), max(indexes))

   def testStructure(self):
      portLayout = PortLayout(
         (Rj45(i) for i in incrange(1, self.nEthernets)),
         (Sfp(i) for i in incrange(
            self.nEthernets + 1,
            self.nEthernets + self.nSfps)),
         (Qsfp(i) for i in incrange(
            self.nEthernets + self.nSfps + 1,
            self.nEthernets + self.nSfps + self.nQsfps)),
         (Osfp(i) for i in incrange(
            self.nEthernets + self.nSfps + self.nQsfps + 1,
            self.nEthernets + self.nSfps + self.nQsfps + self.nOsfps)),
      )
      self._checkPortLayout(portLayout)
