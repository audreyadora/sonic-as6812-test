
from . import Renderer

from ...core.linecard import Linecard

def tryGet(func, default):
   try:
      return func()
   except Exception: # pylint: disable=broad-except
      return default

class ShowCardStatus(Renderer):

   NAME = 'status'

   def getData(self, show):
      data = []
      for card, metadata in show.inventories:
         tmp = {
            'name': str(card),
            'slotId': card.getSlotId(),
            'sku': card.slot.getEeprom().get('SKU'),
            'sid': card.slot.getEeprom().get('SID'),
            'present': tryGet(card.getPresence, False),
            'on': bool(tryGet(card.poweredOn, False)),
         }
         if isinstance(card, Linecard):
            tmp.update({
               'hasCpu': tryGet(card.hasCpuModule, False),
            })
         data.append(tmp)
      return data

   def renderText(self, show):
      data = self.data(show)
      for card in data:
         print(card['name'])
         for k, v in card.items():
            if k != 'name':
               print('  %s: %s' % (k, v))
