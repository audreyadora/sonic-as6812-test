
from ...core.config import Config, tmpfsPath
from ...core.log import getLogger
from ...core.utils import (
   JsonStoredData,
   inSimulation,
   simulateWith,
)
from ...inventory.watchdog import Watchdog
from ...libs.python import monotonicRaw

logging = getLogger(__name__)

class WatchdogState(object):

   STORE_IGNORE = ['localStorage']

   def __init__(self, lastArmed=0, lastTimeout=0, localStorage=None):
      self.lastArmed = lastArmed
      self.lastTimeout = lastTimeout
      if localStorage is not None:
         localStorage = JsonStoredData(localStorage, append=False)
         if not localStorage.writable():
            localStorage = None
      self.localStorage = localStorage

   def __call__(self, lastArmed=0, lastTimeout=0):
      self.lastArmed = lastArmed
      self.lastTimeout = lastTimeout

   def write(self):
      if self.localStorage is None or inSimulation():
         return
      try:
         self.localStorage.writeObj(self)
      except (IOError, OSError):
         logging.error("failed to write watchdog state to cache")

   def read(self):
      if self.localStorage is None or inSimulation():
         return
      try:
         self.localStorage.readObj(self)
      except (IOError, OSError):
         logging.error("failed to read watchdog state from cache")

   def arm(self, timeout):
      self.lastTimeout = timeout
      self.lastArmed = monotonicRaw() if timeout else 0
      self.write()

   def elapsed(self):
      self.read()

      if self.lastArmed == 0:
         return -1

      return int(100 * (monotonicRaw() - self.lastArmed))

   def remaining(self):
      elapsed = self.elapsed() # NOTE: relies on self.read for timeout
      if self.lastTimeout == 0:
         return -1
      return self.lastTimeout - elapsed

class ScdWatchdog(Watchdog):

   MAX_TIMEOUT = 65535

   def __init__(self, scd, reg=0x0120, action=2):
      self.scd = scd
      self.reg = reg
      self.action = action
      self.state = WatchdogState(localStorage=Config().watchdog_state_file)

   def armReg(self, timeout):
      regValue = 0
      if timeout > 0:
         # Set enable bit
         regValue |= 1 << 31
         # Powercycle
         regValue |= self.action << 29
         # Timeout value
         regValue |= timeout
      return regValue

   def armSim(self, timeout):
      if timeout > ScdWatchdog.MAX_TIMEOUT:
         logging.error("watchdog timeout %s exceeds max timeout %s",
                       timeout, ScdWatchdog.MAX_TIMEOUT)
         return False
      if timeout < 0:
         logging.error("watchdog timeout %s must be positive", timeout)
         return False
      regValue = self.armReg(timeout)
      self.state.arm(timeout)
      logging.info("watchdog arm reg={0:32b}".format(regValue))
      return True

   @simulateWith(armSim)
   def arm(self, timeout):
      if timeout > ScdWatchdog.MAX_TIMEOUT:
         logging.error("watchdog timeout %s exceeds max timeout %s",
                       timeout, ScdWatchdog.MAX_TIMEOUT)
         return False

      regValue = self.armReg(timeout)
      try:
         with self.scd.getMmap() as mmap:
            logging.info('arm reg = {0:32b}'.format(regValue))
            mmap.write32(self.reg, regValue)
            self.state.arm(timeout)
      except RuntimeError as e:
         logging.error("watchdog arm/stop error: {}".format(e))
         return False
      return True

   def stopSim(self):
      logging.info("watchdog stop")
      return True

   @simulateWith(stopSim)
   def stop(self):
      return self.arm(0)

   def statusSim(self):
      logging.info("watchdog status")
      return { "enabled": True, "timeout": 300, "remainingTime": 100 }

   @simulateWith(statusSim)
   def status(self):
      try:
         with self.scd.getMmap() as mmap:
            regValue = mmap.read32(self.reg)
            enabled = bool(regValue >> 31)
            timeout = regValue & ((1<<16)-1)

         # No HW support for retrieving remaining time, so it needs to be done
         # here instead. Will only be correct if ran from the same process that
         # armed the watchdog; otherwise the remaining time will be 0.
         if not enabled:
            remainingTime = -1
         else:
            elapsed = self.state.elapsed()
            if timeout != self.state.lastTimeout:
               logging.warning('watchdog: hw (%s) and sw (%s) timeout mismatch',
                               timeout, self.state.lastTimeout)
            remainingTime = 0 if elapsed < 0 else timeout - elapsed

         return {
            "enabled": enabled,
            "timeout": timeout,
            "remainingTime": remainingTime
         }
      except RuntimeError as e:
         logging.error("watchdog status error: {}".format(e))
         return None
