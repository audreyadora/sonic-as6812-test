
from ..core.component.unmanaged import UnmanagedComponent

class PowerDomain(UnmanagedComponent):
   def __init__(self, enabled=None, **kwargs):
      super(PowerDomain, self).__init__(**kwargs)
      self.enabledFn = enabled
      if self.enabledFn is None:
         self.enabledFn = lambda: True

   def isEnabled(self):
      return self.enabledFn()
