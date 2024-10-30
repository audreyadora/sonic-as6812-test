
from . import InventoryInterface, diagcls, diagmethod

@diagcls
class SeuReporter(InventoryInterface):
   @diagmethod('component', fmt=str)
   def getComponent(self):
      raise NotImplementedError

   @diagmethod('seu')
   def hasSeuError(self):
      raise NotImplementedError

   @diagmethod('powercycle')
   def powerCycleOnSeu(self, on=None):
      raise NotImplementedError
