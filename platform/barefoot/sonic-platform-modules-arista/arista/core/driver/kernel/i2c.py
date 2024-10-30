
import os

from ...log import getLogger
from ...utils import inSimulation

from . import KernelDriver

logging = getLogger(__name__)

class I2cKernelDriver(KernelDriver):

   NAME = None

   def __init__(self, addr=None, name=None, **kwargs):
      super(I2cKernelDriver, self).__init__(**kwargs)
      self.addr = addr
      self.name = name or self.NAME

   def setup(self):
      # Load module
      super(I2cKernelDriver, self).setup()

      devPath = self.getSysfsPath()
      path = os.path.join(self.getSysfsBusPath(), 'new_device')
      logging.debug('creating i2c device %s on bus %d at 0x%02x',
                    self.name, self.addr.bus, self.addr.address)
      if inSimulation():
         return
      if os.path.exists(devPath):
         logging.debug('i2c device %s already exists', devPath)
      else:
         with open(path, 'w') as f:
            f.write('%s 0x%02x' % (self.name, self.addr.address))

   def clean(self):
      if inSimulation():
         return

      path = os.path.join(self.getSysfsBusPath(), 'delete_device')
      if os.path.exists(self.getSysfsPath()):
         logging.debug('removing i2c device %s from bus %d at 0x%02x',
                       self.name, self.addr.bus, self.addr.address)
         with open(path, 'w') as f:
            f.write('0x%02x' % self.addr.address)
      else:
         logging.debug('i2c device %s not loaded on bus %d at 0x%02x',
                       self.name, self.addr.bus, self.addr.address)

      # Unload module
      super(I2cKernelDriver, self).clean()

   def getSysfsPath(self):
      return self.addr.getSysfsPath()

   def getSysfsBusPath(self):
      return '/sys/bus/i2c/devices/i2c-%d' % self.addr.bus

   @staticmethod
   def busNameToId(name):
      '''name is assumed to be of the form i2c-X'''
      return int(name[4:])

   def __diag__(self, ctx):
      data = super(I2cKernelDriver, self).__diag__(ctx)
      data.update({
         'addr': str(self.addr),
         'name': self.name,
      })
      return data
