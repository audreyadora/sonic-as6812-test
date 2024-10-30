
from . import InventoryInterface, diagcls, diagmethod

@diagcls
class Programmable(InventoryInterface):
   @diagmethod('component', fmt=str)
   def getComponent(self):
      raise NotImplementedError

   @diagmethod('version', io=True)
   def getVersion(self):
      raise NotImplementedError

   @diagmethod('description')
   def getDescription(self):
      raise NotImplementedError
