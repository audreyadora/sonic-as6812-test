from ..core.desc import HwDesc

class ResetDesc(HwDesc):
   def __init__(self, name, addr=None, bit=None, activeLow=False, auto=True,
                **kwargs):
      super(ResetDesc, self).__init__(**kwargs)
      self.name = name
      self.addr = addr
      self.bit = bit
      self.activeLow = activeLow
      self.auto = auto
