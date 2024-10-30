
from . import InventoryInterface, diagcls, diagmethod

@diagcls
class Interrupt(InventoryInterface):
   # TODO: get ?

   def set(self):
      raise NotImplementedError()

   def clear(self):
      raise NotImplementedError()

   @diagmethod('name')
   def getName(self):
      raise NotImplementedError()

   @diagmethod('file')
   def getFile(self):
      raise NotImplementedError()
