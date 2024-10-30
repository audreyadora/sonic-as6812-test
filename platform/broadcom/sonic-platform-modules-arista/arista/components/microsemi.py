
from ..core.component import Priority
from ..core.pci import PciSwitch, DownstreamPciPort

from ..drivers.microsemi import MicrosemiDriver
from ..drivers.pci import PciSwitchPortDriver

class MicrosemiPortDesc(object):
   def __init__(self, port, dsp, partition):
      self.port = port
      self.dsp = dsp
      self.partition = partition

class MicrosemiPort(DownstreamPciPort):

   DRIVER = PciSwitchPortDriver
   PRIORITY = Priority.DEFAULT

   def __init__(self, port=0, desc=None, **kwargs):
      super(MicrosemiPort, self).__init__(port=port, **kwargs)
      self.desc = desc

   def enable(self):
      self.driver.enable()

   def disable(self):
      self.driver.disable()

   def bind(self):
      return self.parent.bind(self)

   def unbind(self):
      return self.parent.unbind(self)

class Microsemi(PciSwitch):

   DRIVER = MicrosemiDriver
   PRIORITY = Priority.DEFAULT

   DOWNSTREAM_PORT_CLS = MicrosemiPort

   def addPciPort(self, desc=None, **kwargs):
      return self.downstreamPort(port=desc.port, device=desc.dsp - 1, desc=desc, **kwargs)

   def bind(self, port):
      desc = port.desc
      return self.driver.bind(desc.port, desc.dsp, desc.partition)

   def unbind(self, port, flags=0x2):
      desc = port.desc
      return self.driver.unbind(desc.dsp, desc.partition, flags=flags)
