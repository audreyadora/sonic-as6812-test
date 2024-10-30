
from .component import Component

class SlotComponent(Component):
   def getPresence(self):
      raise NotImplementedError
