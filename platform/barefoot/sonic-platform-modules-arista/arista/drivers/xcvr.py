import os

from ..core.driver.kernel.i2c import I2cKernelDriver
from ..core.utils import inSimulation

class XcvrKernelDriver(I2cKernelDriver):
   MODULE = 'optoe'

   def __init__(self, portName=None, **kwargs):
      super(XcvrKernelDriver, self).__init__(**kwargs)
      self.portName = portName

   def setup(self):
      super(XcvrKernelDriver, self).setup()

      if inSimulation():
         return

      self.setPortName(self.portName)

   def setPortName(self, name):
      portNamePath = os.path.join(self.getSysfsPath(), 'port_name')
      with open(portNamePath, 'w') as f:
         f.write(name)

   def setWriteMax(self, size):
      writeMaxPath = os.path.join(self.getSysfsPath(), 'write_max')
      if os.path.exists(writeMaxPath):
         with open(writeMaxPath, 'w') as f:
            f.write(str(size))

   def getWriteMax(self):
      writeMaxPath = os.path.join(self.getSysfsPath(), 'write_max')
      if not os.path.exists(writeMaxPath):
         return 1 # NOTE: previous version of the driver hardcoded 1
      with open(writeMaxPath) as f:
         return int(f.read())

class SfpKernelDriver(XcvrKernelDriver):
   NAME = 'optoe2'

class QsfpKernelDriver(XcvrKernelDriver):
   NAME = 'optoe1'

class OsfpKernelDriver(XcvrKernelDriver):
   NAME = 'optoe3'
