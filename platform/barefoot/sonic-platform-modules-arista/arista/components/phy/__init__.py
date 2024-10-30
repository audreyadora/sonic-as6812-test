
from ...inventory.phy import Phy

class PhyImpl(Phy):
   def __init__(self, phyId, reset=None):
      self.id = phyId
      self.reset = reset

   def getReset(self):
      return self.reset

class MdioPhy(PhyImpl):
   def __init__(self, phyId, mdios, reset=None):
      super(MdioPhy, self).__init__(phyId, reset=reset)
      self.mdios = mdios

   def getMdios(self):
      return self.mdios
