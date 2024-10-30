
from . import InventoryInterface, diagcls, diagmethod

@diagcls
class Rail(InventoryInterface):
   @diagmethod('name')
   def getName(self):
      raise NotImplementedError

   @diagmethod('power', io=True)
   def getPower(self):
      raise NotImplementedError

   @diagmethod('current', io=True)
   def getCurrent(self):
      raise NotImplementedError

   @diagmethod('voltage', io=True)
   def getVoltage(self):
      raise NotImplementedError
