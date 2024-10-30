
from . import InventoryInterface, diagcls, diagmethod

@diagcls
class Xcvr(InventoryInterface):

   ADDR = 0x50

   @diagmethod('type')
   def getType(self):
      raise NotImplementedError

   @diagmethod('name')
   def getName(self):
      raise NotImplementedError

   @diagmethod('id')
   def getId(self):
      raise NotImplementedError

   @diagmethod('addr', fmt=str)
   def getI2cAddr(self):
      raise NotImplementedError

class Ethernet(Xcvr): # pylint: disable=abstract-method
   pass

class Sfp(Xcvr): # pylint: disable=abstract-method
   pass

class Qsfp(Xcvr): # pylint: disable=abstract-method
   pass

class Osfp(Xcvr): # pylint: disable=abstract-method
   pass

@diagcls
class XcvrSlot(InventoryInterface):
   @diagmethod('id')
   def getId(self):
      raise NotImplementedError

   @diagmethod('name')
   def getName(self):
      raise NotImplementedError

   @diagmethod('present', io=True)
   def getPresence(self):
      raise NotImplementedError

   @diagmethod('leds', diag=True)
   def getLeds(self):
      raise NotImplementedError

   @diagmethod('lpmode', io=True)
   def getLowPowerMode(self):
      raise NotImplementedError

   def setLowPowerMode(self, value):
      raise NotImplementedError

   @diagmethod('modsel', io=True)
   def getModuleSelect(self):
      raise NotImplementedError

   def setModuleSelect(self, value):
      raise NotImplementedError

   @diagmethod('intr', diag=True)
   def getInterruptLine(self):
      raise NotImplementedError

   @diagmethod('reset', diag=True)
   def getReset(self):
      raise NotImplementedError

   @diagmethod('rxlos', io=True)
   def getRxLos(self):
      raise NotImplementedError

   @diagmethod('txdisable', io=True)
   def getTxDisable(self):
      raise NotImplementedError

   def setTxDisable(self, value):
      raise NotImplementedError

   @diagmethod('txfault', io=True)
   def getTxFault(self):
      raise NotImplementedError

   @diagmethod('xcvr', diag=True)
   def getXcvr(self):
      raise NotImplementedError

class EthernetSlot(XcvrSlot): # pylint: disable=abstract-method
   NUM_CHANNELS = 1

class SfpSlot(XcvrSlot): # pylint: disable=abstract-method
   NUM_CHANNELS = 1

class QsfpSlot(XcvrSlot): # pylint: disable=abstract-method
   NUM_CHANNELS = 4

class OsfpSlot(XcvrSlot): # pylint: disable=abstract-method
   NUM_CHANNELS = 8
