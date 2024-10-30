
from ..core.desc import HwDesc

class GpioDesc(HwDesc):
   def __init__(self, name, addr=None, bit=None, ro=False, activeLow=False,
                **kwargs):
      super(GpioDesc, self).__init__(**kwargs)

      self.name = name
      self.addr = addr
      self.bit = bit
      self.ro = ro
      self.activeLow = activeLow
