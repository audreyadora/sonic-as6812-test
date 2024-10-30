
from . import InventoryInterface, diagcls, diagmethod

@diagcls
class Phy(InventoryInterface):
   @diagmethod('reset', diag=True)
   def getReset(self):
      raise NotImplementedError
