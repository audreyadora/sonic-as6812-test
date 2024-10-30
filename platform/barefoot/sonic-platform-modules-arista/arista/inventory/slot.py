
from . import InventoryInterface, diagcls, diagmethod

@diagcls
class Slot(InventoryInterface):
   @diagmethod('present', io=True)
   def getPresence(self):
      raise NotImplementedError
