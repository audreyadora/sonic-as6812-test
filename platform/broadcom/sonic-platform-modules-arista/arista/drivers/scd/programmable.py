
from ...inventory.programmable import Programmable

class ScdProgrammable(Programmable):
   def __init__(self, scd):
      self.scd = scd

   def getComponent(self):
      return self.scd

   def getDescription(self):
      return 'System Control Device'

   def getVersion(self):
      return self.scd.getVersion()
