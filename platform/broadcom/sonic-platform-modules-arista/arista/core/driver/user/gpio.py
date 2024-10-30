from ...utils import inSimulation

from ....inventory.gpio import Gpio

class GpioFuncImpl(Gpio):
   # TODO Remove name arg and make desc positional
   def __init__(self, driver, func, desc=None, name=None, hwActiveLow=False,
                **kwargs):
      self.driver = driver
      self.func = func
      self.addr = desc.addr if desc else 0
      self.bit = desc.bit if desc else 0
      self.name = desc.name if desc else name
      self.ro = desc.ro if desc else False
      self.activeLow = desc.activeLow if desc else False
      self.hwActiveLow = hwActiveLow
      self.__dict__.update(**kwargs)

   def getName(self):
      return self.name

   def getAddr(self):
      return self.addr

   def getPath(self):
      return None

   def getBit(self):
      return self.bit

   def isRo(self):
      return self.ro

   def isActiveLow(self):
      return False if self.hwActiveLow else self.activeLow

   def getRawValue(self):
      return self.func()

   def setRawValue(self, value):
      return self.func(value)

   def _activeValue(self):
      return 0 if self.isActiveLow() else 1

   def isActive(self):
      if inSimulation():
         return True
      return self.getRawValue() == self._activeValue()

   def setActive(self, value):
      self.setRawValue(not value if self.isActiveLow() else value)

   def resetIn(self):
      return self.setActive(True)

   def resetOut(self):
      return self.setActive(False)

   def read(self):
      return self.isActive()
