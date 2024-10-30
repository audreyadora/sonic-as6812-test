import os

from ..core.config import flashPath
from ..core.driver.user import UserDriver

class SonicReloadCauseCookieDriver(UserDriver):
   def __init__(self, slotId=None, filePath=None, **kwargs): # pylint: disable=unused-argument
      super().__init__(**kwargs)
      self.filePath = filePath or flashPath('reboot-cause/reboot-cause.txt')

   def getSoftwareCause(self):
      if os.path.exists(self.filePath):
         with open(self.filePath, 'r', encoding='utf-8') as f:
            return f.readline()
      return None
