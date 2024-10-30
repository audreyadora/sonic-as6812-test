
from ...core.diag import DiagContext

from . import Renderer, Table, Col

class ShowXcvr(Renderer):

   NAME = 'xcvr'

   def getData(self, show):
      ctx = DiagContext()
      data = []
      for inventory, _ in show.inventories:
         for name, xcvr in inventory.getXcvrSlots().items():
            data.append(xcvr.__diag__(ctx))
      return data

   def renderText(self, show):
      data = self.data(show)

      Table([
         Col('Id', 'id', 3),
         Col('Type', 'xcvr.type', 7),
         Col('Present', 'present', 7),
         Col('LpMode', 'lpmode', 6),
         Col('Reset', 'reset.value', 6),
         Col('TxDisable', 'txdisable', 9),
         Col('TxFault', 'txfault', 7),
         Col('RxLos', 'rxlos', 5),
         Col('Addr', 'xcvr.addr', 7),
      ]).render(data)
