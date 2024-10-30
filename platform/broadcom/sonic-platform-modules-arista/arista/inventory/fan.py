
from . import InventoryInterface, diagcls, diagmethod

@diagcls
class Fan(InventoryInterface):
   @diagmethod('id')
   def getId(self):
      raise NotImplementedError

   @diagmethod('name')
   def getName(self):
      raise NotImplementedError

   @diagmethod('model')
   def getModel(self):
      raise NotImplementedError

   @diagmethod('rpm')
   def getRpm(self):
      raise NotImplementedError

   @diagmethod('speed', io=True)
   def getSpeed(self):
      raise NotImplementedError

   def setSpeed(self, speed):
      raise NotImplementedError

   @diagmethod('direction', io=True)
   def getDirection(self):
      raise NotImplementedError

   @diagmethod('fault', io=True)
   def getFault(self):
      raise NotImplementedError

   @diagmethod('status', io=True)
   def getStatus(self):
      raise NotImplementedError

   @diagmethod('position', io=True)
   def getPosition(self):
      raise NotImplementedError

   def getLed(self):
      raise NotImplementedError

@diagcls
class FanSlot(InventoryInterface):
   @diagmethod('id')
   def getId(self):
      raise NotImplementedError

   @diagmethod('name')
   def getName(self):
      raise NotImplementedError

   @diagmethod('model')
   def getModel(self):
      raise NotImplementedError

   @diagmethod('present', io=True)
   def getPresence(self):
      raise NotImplementedError

   @diagmethod('fans', diag=True)
   def getFans(self):
      raise NotImplementedError

   @diagmethod('direction', io=True)
   def getDirection(self):
      raise NotImplementedError

   def getLed(self):
      raise NotImplementedError

   @diagmethod('fault', io=True)
   def getFault(self):
      raise NotImplementedError

   @diagmethod('maxPowerDraw')
   def getMaxPowerDraw(self):
      raise NotImplementedError
