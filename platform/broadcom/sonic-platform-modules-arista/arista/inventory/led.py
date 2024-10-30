
from . import InventoryInterface, diagcls, diagmethod

@diagcls
class Led(InventoryInterface):
   @diagmethod('name')
   def getName(self):
      raise NotImplementedError

   @diagmethod('color', io=True)
   def getColor(self):
      raise NotImplementedError

   def setColor(self, color):
      raise NotImplementedError

   @diagmethod('isStatus')
   def isStatusLed(self):
      raise NotImplementedError
