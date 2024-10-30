
from . import registerAction
from ....args.show.fabric.status import statusParser
from ....show.card import ShowCardStatus

@registerAction(statusParser)
def doShowStatus(ctx, args):
   for fabric in ctx.fabrics:
      ctx.show.addInventory(fabric)
   ctx.show.render(ShowCardStatus())
