from ..descs.xcvr import Osfp, Qsfp, QsfpDD, Rj45, Sfp

class PortLayout():
   def __init__(self, *args):
      self.ports = [p for pgen in args for p in pgen]

   def getEthernets(self):
      return [p for p in self.ports if isinstance(p, Rj45)]

   def getSfps(self):
      return [p for p in self.ports if isinstance(p, Sfp)]

   def getQsfps(self):
      return [p for p in self.ports if
               isinstance(p, Qsfp) and not isinstance(p, QsfpDD)]

   def getOsfps(self):
      return [p for p in self.ports if isinstance(p, (Osfp, QsfpDD))]

   def getAllPorts(self):
      return self.ports

   def getPorts(self, *args):
      return [p for p in self.ports if isinstance(p, args)]

   def getPort(self, index):
      filtered = [p for p in self.ports if p.index == index]
      if not filtered:
         return None
      return filtered[0]
