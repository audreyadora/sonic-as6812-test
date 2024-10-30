from . import InventoryInterface, diagcls, diagmethod

@diagcls
class Gpio(InventoryInterface):
   @diagmethod('name')
   def getName(self):
      raise NotImplementedError

   @diagmethod('addr', fmt=hex)
   def getAddr(self):
      raise NotImplementedError

   @diagmethod('path')
   def getPath(self):
      raise NotImplementedError

   @diagmethod('bit')
   def getBit(self):
      raise NotImplementedError

   @diagmethod('ro')
   def isRo(self):
      raise NotImplementedError

   @diagmethod('activeLow')
   def isActiveLow(self):
      raise NotImplementedError

   @diagmethod('rawValue', io=True)
   def getRawValue(self):
      raise NotImplementedError

   def setRawValue(self, value):
      raise NotImplementedError

   @diagmethod('active', io=True)
   def isActive(self):
      raise NotImplementedError

   def setActive(self, value):
      raise NotImplementedError
