
from ...tests.testing import unittest

from ..pci import (
   DownstreamPciPort,
   PciBridge,
   PciRoot,
   UpstreamPciPort,
)

class MockDownstreamPciPort(DownstreamPciPort):
   pass

class MockUpstreamPciPort(UpstreamPciPort):
   pass

class MockPciBridge(PciBridge):
   DOWNSTREAM_PORT_CLS = MockDownstreamPciPort
   UPSTREAM_PORT_CLS = MockUpstreamPciPort

class MockPciRoot(PciRoot):
   pass

class PciTest(unittest.TestCase):
   def _validatePort(self, port, parent=None, cls=None):
      self.assertIsNotNone(port)
      self.assertIsNotNone(port.parent)
      self.assertIsNotNone(port.addr)
      self.assertIsNotNone(port.upstream)
      str(port.addr)
      port.addr.getSysfsPath()
      if parent is not None:
         self.assertEqual(port.upstream, parent)
      if cls is not None:
         self.assertIsInstance(port, cls)

   def testRootPort(self, root=None):
      # Endpoint directly attached to a root port (e.g LPC SCD)
      # pci0000:ff/ (root)
      #   0000:ff:01.3/ (endpoint)
      root = root or MockPciRoot()
      rp1 = root.rootPort(bus=0xff, device=1, func=3)
      self._validatePort(rp1)
      self.assertEqual(rp1, root.rootPort(bus=0xff, device=1, func=3))
      self.assertIn(rp1.parent, root.roots.values())

   def testBridgeRootPort(self, root=None):
      # Endpoint attached to a bridge attached to a root port (e.g PCI SCD)
      # pci0000:00/ (root)
      #   0000:00:1c.0/ (bridge)
      #     0000:9f:00.0/ (endpoint port:0)
      root = root or MockPciRoot()
      rp1 = root.rootPort(device=0x1c)
      rp1.secondary_ = 0x9f
      ep1 = rp1.pciEndpoint(port=0)
      self._validatePort(rp1)
      self._validatePort(ep1, rp1)
      self.assertEqual(rp1, root.rootPort(device=0x1c))
      self.assertEqual(ep1, rp1.pciEndpoint(port=0))
      self.assertIn(rp1.parent, root.roots.values())

   def testComplexTree(self, root=None):
      # More complex topology
      # pci0000:00/ (root)
      #   0000:00:03.0/ (bridge)
      #     0000:05:00.0/ (bridge upstream port:0)
      #       0000:06:00.0/ (bridge downstream port:0)
      #         0000:07:00.0/ (bridge2 upstream)
      #           0000:08:00.0/ (bridge2 downstream port:0)
      #             0000:09:00.0 (ep1)
      #           0000:08:01.0/ (bridge2 downstream port:1)
      #             0000:0a:00.0 (ep2
      #       0000:06:01.0/ (bridge downstream port:1)
      #     0000:05:00.1/ (endpoint port:0)
      root = root or MockPciRoot()

      rp1 = root.rootPort(device=0x03)
      rp1.secondary_ = 0x05
      self._validatePort(rp1)

      br1 = MockPciBridge()
      up1 = br1.upstreamPort()
      up1.secondary_ = 0x06
      self.assertEqual(up1, br1.upstreamPort())
      rp1.attach(up1)
      self._validatePort(up1, rp1, UpstreamPciPort)
      dp1 = br1.downstreamPort(port=0)
      dp1.secondary_ = 0x07
      self._validatePort(dp1, up1, DownstreamPciPort)
      dp2 = br1.downstreamPort(port=1, device=1)
      dp2.secondary_ = 0x10
      self._validatePort(dp2, up1, DownstreamPciPort)

      br2 = MockPciBridge()
      up2 = br2.upstreamPort()
      up2.secondary_ = 0x08
      self.assertEqual(up2, br2.upstreamPort())
      dp1.attach(up2)
      self._validatePort(up2, dp1, UpstreamPciPort)
      dp3 = br2.downstreamPort(port=0)
      dp3.secondary_ = 0x09
      self._validatePort(dp3, up2, DownstreamPciPort)
      dp4 = br2.downstreamPort(port=1, device=1)
      dp4.secondary_ = 0x0a
      self._validatePort(dp4, up2, DownstreamPciPort)

      ep1 = dp3.pciEndpoint(port=0)
      self._validatePort(ep1, dp3, UpstreamPciPort)
      ep2 = dp4.pciEndpoint(port=1)
      self._validatePort(ep2, dp4, UpstreamPciPort)

   def testAllPciTopology(self):
      root = MockPciRoot()
      self.testRootPort(root)
      self.assertEqual(len(root.roots), 1)
      self.testBridgeRootPort(root)
      self.assertEqual(len(root.roots), 2)
      self.testComplexTree(root)
      self.assertEqual(len(root.roots), 2)

if __name__ == '__main__':
   unittest.main()
