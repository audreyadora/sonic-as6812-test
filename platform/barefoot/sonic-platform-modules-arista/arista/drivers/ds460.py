from contextlib import closing

from ..core import utils
from ..core.log import getLogger

from .pmbus import PmbusKernelDriver

logging = getLogger(__name__)

class Ds460KernelDriver(PmbusKernelDriver):

   NAME = 'dps460'

   def setup(self):
      addr = self.addr.address

      logging.debug('%s: initializing registers', self.name)
      with closing(utils.SMBus(self.addr.bus)) as bus:
         for _ in utils.Retrying(interval=10.0, delay=0.5):
            try:
               bus.read_byte_data(addr, 0x00)
               logging.debug('%s: device accessible: bus=%s',
                             self.name, self.addr.bus)
               break
            except IOError:
               logging.debug('%s: device not accessible; retrying...', self.name)
         else:
            logging.error('%s: failed to access device: bus=%s',
                          self.name, self.addr.bus)
            return

         try:
            byte = bus.read_byte_data(addr, 0x10)
            bus.write_byte_data(addr, 0x10, 0)
            bus.write_byte_data(addr, 0x03, 1)
            bus.write_byte_data(addr, 0x10, byte)
         except IOError:
            logging.debug('%s: failed to initialize', self.name)

      super(Ds460KernelDriver, self).setup()
