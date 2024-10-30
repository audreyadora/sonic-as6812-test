
from __future__ import absolute_import, division, print_function

from ...tests.testing import unittest, patch
from ...core.fixed import FixedSystem
from ...core.platform import loadPlatforms, getPlatforms
from ...core.pci import (
   DownstreamPciPort,
   PciBridge,
   PciPort,
   PciRoot,
   PciSwitch,
   PciSysfsPath,
   RootPciBridge,
   RootPciPort,
   UpstreamPciPort,
)


class ComponentTest(unittest.TestCase):
   def testSetup(self):
      loadPlatforms()
      for platformCls in getPlatforms():
         if not issubclass(platformCls, FixedSystem):
            continue
         platform = platformCls()

         mocks = []
         for c in platform.iterComponents():
            mocks.append(patch.object(c, 'setup').start())

         platform.setup()

         for mock in mocks:
            if hasattr(mock, 'assert_called_once'):
               # python2 mock version can be outdated, it will be check by py3
               mock.assert_called_once()

   def testPciAddrDuplication(self):
      pciElements = (
         DownstreamPciPort,
         PciBridge,
         PciPort,
         PciRoot,
         PciSwitch,
         RootPciBridge,
         RootPciPort,
         UpstreamPciPort
      )
      loadPlatforms()
      for platformCls in getPlatforms():
         if not issubclass(platformCls, FixedSystem):
            continue
         platform = platformCls()
         sysfsSet = set()
         for c in platform.iterComponents(filters=None):
            if not isinstance(c, pciElements) and isinstance(c.addr, PciSysfsPath):
               sysfsPath = c.addr.getSysfsPath()
               self.assertNotIn(sysfsPath, sysfsSet)
               sysfsSet.add(sysfsPath)

if __name__ == '__main__':
   unittest.main()
