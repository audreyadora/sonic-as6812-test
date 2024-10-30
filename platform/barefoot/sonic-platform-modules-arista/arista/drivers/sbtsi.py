
from ..core.driver.user.i2c import I2cDevDriver
from ..core.register import Register, RegisterMap, RegBitRange, RegBitField

from ..inventory.temp import Temp

class SbTsiTemp(Temp):
   def __init__(self, driver, desc, **kwargs):
      self.driver = driver
      self.desc = desc

   def getName(self):
      return self.desc.name

   def getPresence(self):
      return True

   def getDesc(self):
      return self.desc

   def getModel(self):
      return 'SBTSI'

   def getStatus(self):
      return True

   def getTemperature(self):
      return self.driver.getTemperature()

   def getHighThreshold(self):
      return self.driver.getHighThreshold()

   def setHighThreshold(self, value):
      self.driver.setHighThreshold(value)

   def getHighCriticalThreshold(self):
      return self.desc.critical

   def getLowCriticalThreshold(self):
      return self.desc.lcritical

   def getLowThreshold(self):
      return self.driver.getLowThreshold()

   def setLowThreshold(self, value):
      self.driver.setLowThreshold(value)

   def refreshHardwareThresholds(self):
      self.setLowThreshold(self.desc.low)
      self.setHighThreshold(self.desc.overheat)

class SbTsiRegisterMap(RegisterMap):
   CPU_TEMP_INT = Register(0x01, name='cpuTempInt')
   STATUS = Register(0x02,
      RegBitField(3, name='cpuTempLow'),
      RegBitField(4, name='cpuTempHigh'),
   )
   HI_TEMP_INT = Register(0x07, name='hiTempInt', ro=False)
   LO_TEMP_INT = Register(0x08, name='loTempInt', ro=False)
   CPU_TEMP_DEC = Register(0x10,
      RegBitRange(5, 7, name='cpuTempDec')
   )
   CPU_TEMP_OFF_INT = Register(0x11, name='cpuTempOffInt', ro=False)
   CPU_TEMP_OFF_DEC = Register(0x12, name='cpuTempOffDec', ro=False)
   HI_TEMP_DEC = Register(0x13,
      RegBitRange(5, 7, name='hiTempDec', ro=False)
   )
   LO_TEMP_DEC = Register(0x14,
      RegBitRange(5, 7, name='loTempDec', ro=False)
   )

class SbTsiUserDriver(I2cDevDriver):

   REGISTER_CLS = SbTsiRegisterMap

   def _tempVal(self, i, d):
      return i + d * 0.125

   def _setThresh(self, ir, dr, value):
      ir(int(value))
      dr(int((value - int(value)) / 0.125))

   def getHighThreshold(self):
      return self._tempVal(self.regs.hiTempInt(), self.regs.hiTempDec())

   def setHighThreshold(self, value):
      self._setThresh(self.regs.hiTempInt, self.regs.hiTempDec, value)

   def getLowThreshold(self):
      return self._tempVal(self.regs.loTempInt(), self.regs.loTempDec())

   def setLowThreshold(self, value):
      self._setThresh(self.regs.loTempInt, self.regs.loTempDec, value)

   def getTemperature(self):
      return self._tempVal(self.regs.cpuTempInt(), self.regs.cpuTempDec())

   def getTempSensor(self, desc, **kwargs):
      return SbTsiTemp(self, desc, **kwargs)
