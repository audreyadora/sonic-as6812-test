
from . import InventoryInterface, diagcls, diagmethod

@diagcls
class Reset(InventoryInterface):
   @diagmethod('name')
   def getName(self):
      raise NotImplementedError

   @diagmethod('value', io=True)
   def read(self):
      raise NotImplementedError

   def resetIn(self):
      raise NotImplementedError

   def resetOut(self):
      raise NotImplementedError
