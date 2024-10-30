
from ..core.config import Config
from ..inventory.watchdog import Watchdog
from ..drivers.scd.watchdog import WatchdogState

class FakeWatchdog(Watchdog):

   MAX_TIMEOUT = 65535

   def __init__(self):
      self.state = WatchdogState(localStorage=Config().watchdog_state_file)

   def arm(self, timeout):
      self.state.arm(timeout)
      return True

   def stop(self):
      self.state.arm(0)
      return True

   def status(self):
      remaining = self.state.remaining()
      return {
         'enabled': self.state.lastArmed != 0,
         'timeout': self.state.lastTimeout,
         'remainingTime': remaining,
      }
