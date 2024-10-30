
from . import InventoryInterface, diagcls, diagmethod

@diagcls
class Watchdog(InventoryInterface):
   def arm(self, timeout):
      raise NotImplementedError

   def stop(self):
      raise NotImplementedError

   @diagmethod('status', io=True)
   def status(self):
      raise NotImplementedError
