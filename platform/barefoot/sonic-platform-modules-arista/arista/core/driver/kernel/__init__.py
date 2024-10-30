
import os

from .. import (
   Driver,
   deviceListForModule,
   isModuleLoaded,
   modprobe,
   rmmod,
)
from ...log import getLogger
from ...utils import inSimulation
from .. import utils

from ....libs.retry import tryGet

from .sysfs import (
   FanSysfsImpl,
   GpioSysfsImpl,
   LedSysfsImpl,
   RailSysfsImpl,
   ResetSysfsImpl,
   TempSysfsImpl,
)

logging = getLogger(__name__)

class KernelDriver(Driver):

   MODULE = None
   ARGS = []
   PATH = None
   PASSIVE = False

   def __init__(self, module=None, margs=None, **kwargs):
      super(KernelDriver, self).__init__(**kwargs)
      self.margs = margs if margs is not None else self.ARGS
      self.module = module or self.MODULE
      self.hwmonPath = None

   def __str__(self):
      return '%s(module=%s)' % (self.__class__.__name__, self.module)

   def setup(self):
      if self.PASSIVE:
         return
      if not self.loaded():
         modprobe(self.module, self.margs)

   def clean(self):
      if self.PASSIVE:
         return

      if not self.loaded():
         logging.debug('Module %s is not loaded', self.module)
         return

      devices = deviceListForModule(self.module)
      if devices:
         logging.debug('Module %s is still in use by other devices: %s',
                       self.module, devices)
         return

      try:
         rmmod(self.module)
      except Exception as e: # pylint: disable=broad-except
         logging.error('Failed to unload %s: %s', self.module, e)

   def loaded(self):
      return isModuleLoaded(self.module)

   def getSysfsPath(self):
      if self.PATH is not None:
         return self.PATH
      raise NotImplementedError

   def getHwmonPath(self):
      if self.hwmonPath is None:
         self.hwmonPath = utils.locateHwmonFolder(self.getSysfsPath())
      return self.hwmonPath

   def getHwmonEntry(self, entry):
      return os.path.join(self.getHwmonPath(), entry)

   def __diag__(self, ctx):
      return {
         "module": self.module,
         "args": self.margs,
         "sysfs": tryGet(self.getSysfsPath, default=None),
      }

   # Helpers for most drivers

   def getFan(self, desc, **kwargs):
      return FanSysfsImpl(self, desc, **kwargs)

   def getFanLed(self, desc, **kwargs):
      return LedSysfsImpl(self, desc, **kwargs)

   def getLed(self, desc, **kwargs):
      return LedSysfsImpl(self, desc, **kwargs)

   def getTempSensor(self, desc, **kwargs):
      return TempSysfsImpl(self, desc, **kwargs)

   def getReset(self, desc, **kwargs):
      return ResetSysfsImpl(self, desc, **kwargs)

   def getGpio(self, desc, **kwargs):
      return GpioSysfsImpl(self, desc, **kwargs)

   def getRail(self, desc, **kwargs):
      return RailSysfsImpl(self, desc, **kwargs)
