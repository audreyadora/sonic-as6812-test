
class DenaliAsicDesc(object):
   def __init__(self, cls=None, asicId=None, rstIdx=None):
      self.cls = cls
      self.asicId = asicId
      self.rstIdx = rstIdx or asicId
