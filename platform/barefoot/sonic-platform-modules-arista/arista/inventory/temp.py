
from . import InventoryInterface, diagcls, diagmethod

@diagcls
class Temp(InventoryInterface):
   @diagmethod('name')
   def getName(self):
      raise NotImplementedError

   def getDesc(self):
      raise NotImplementedError

   @diagmethod('present')
   def getPresence(self):
      raise NotImplementedError

   @diagmethod('model')
   def getModel(self):
      raise NotImplementedError

   @diagmethod('status', io=True)
   def getStatus(self):
      raise NotImplementedError

   @diagmethod('value', io=True)
   def getTemperature(self):
      raise NotImplementedError

   @diagmethod('lowThresh', io=True)
   def getLowThreshold(self):
      raise NotImplementedError

   @diagmethod('lowCritThresh', io=True)
   def getLowCriticalThreshold(self):
      raise NotImplementedError

   @diagmethod('highThresh', io=True)
   def getHighThreshold(self):
      raise NotImplementedError

   @diagmethod('highCritThresh', io=True)
   def getHighCriticalThreshold(self):
      raise NotImplementedError

   def setLowThreshold(self, value):
      raise NotImplementedError

   def setLowCriticalThreshold(self, value):
      raise NotImplementedError

   def setHighThreshold(self, value):
      raise NotImplementedError

   def setHighCriticalThreshold(self, value):
      raise NotImplementedError

   def refreshHardwareThresholds(self):
      raise NotImplementedError
