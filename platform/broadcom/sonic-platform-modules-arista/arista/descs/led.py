
from ..core.desc import HwDesc

class LedColor(object):
   GREEN = 'green'
   RED = 'red'
   AMBER = 'amber'
   BLUE = 'blue'
   OFF = 'off'

class LedDesc(HwDesc):
   def __init__(self, name=None, colors=None, blinking=False, **kwargs):
      super(LedDesc, self).__init__(**kwargs)
      self.name = name
      self.colors = colors
      self.blinking = blinking
