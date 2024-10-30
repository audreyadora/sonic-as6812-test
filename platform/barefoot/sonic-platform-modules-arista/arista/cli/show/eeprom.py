
from . import Renderer

class ShowEeprom(Renderer):

   NAME = 'eeprom'

   def getData(self, show):
      ret = []
      for inventory, metadata in show.inventories:
         inventory.update(metadata)
         ret += [inventory]
      return ret

   def renderText(self, show):
      data = self.data(show)

      t = ['\n'.join(['%s: %s' % (k, v) for k, v in d.items()]) for d in data]
      print('\n\n'.join(t))
