
from ...inventory.seu import SeuReporter

class ScdSeuReporter(SeuReporter):
   def __init__(self, scd, regmap):
      self.scd = scd
      self.regmap = regmap
      self.regs_ = None

   def __str__(self):
      return self.__class__.__name__

   @property
   def regs(self):
      if self.regs_ is None:
         self.regs_ = self.regmap(self.scd.driver)
      return self.regs_

   def getComponent(self):
      return self.scd

   def hasSeuError(self):
      return bool(self.regs.hasSeuError())

   def powerCycleOnSeu(self, on=None):
      if not hasattr(self.regs, 'powerCycleOnSeu'):
         return False
      return bool(self.regs.powerCycleOnSeu(value=on))
