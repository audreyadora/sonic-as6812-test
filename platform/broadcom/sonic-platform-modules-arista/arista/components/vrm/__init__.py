
from ...core.component.i2c import I2cComponent
from ...core.log import getLogger

from ...drivers.vrm import VrmI2cUserDriver

logging = getLogger(__name__)

class Vrm(I2cComponent):
   DRIVER = VrmI2cUserDriver

   class Registers(object):
      VOUT_COMMAND = 0x21
      UV_WARNING = 0x43
      UV_FAULT = 0x44

   def __init__(self, vouts=None, uvs=None, identify=None, **kwargs):
      super().__init__(**kwargs)
      self.vouts = vouts
      self.uvs = uvs
      if identify:
         self.driver.IDENTIFY_SEQUENCE = identify

   def identify(self):
      return self.driver.identify()

   def setUnderVoltageWarning(self, value):
      logging.debug('Configuring %s UV Warning to 0x%04x', self, value)
      self.driver.write_word_data(self.Registers.UV_WARNING, value)

   def setUnderVoltageFault(self, value):
      logging.debug('Configuring %s UV Fault to 0x%04x', self, value)
      self.driver.write_word_data(self.Registers.UV_FAULT, value)

   def updateThresholds(self):
      if self.uvs is None:
         return

      warning, fault = self.uvs
      if warning is not None:
         self.setUnderVoltageWarning(warning)
      if fault is not None:
         self.setUnderVoltageFault(fault)

   def voutCommand(self, vout):
      logging.debug('Configuring %s VOUT to 0x%04x', self, vout)
      # TODO: use RegisterMap when variable size registers are supported
      self.driver.write_word_data(self.Registers.VOUT_COMMAND, vout)

   def setVoutValue(self, value):
      self.updateThresholds()
      self.voutCommand(self.vouts[value])

class VrmNotFoundError(Exception):
   pass

class VrmDetector(object):
   def __init__(self, vrms):
      self.vrms = vrms
      self.vrm_ = None

   def __str__(self):
      return self.__class__.__name__

   def identifyVrm(self):
      for vrm in self.vrms:
         if vrm.identify():
            logging.debug('%s: found VRM %s', self, vrm)
            return vrm
      raise VrmNotFoundError

   @property
   def vrm(self):
      if self.vrm_ is None:
         self.vrm_ = self.identifyVrm()
      return self.vrm_
