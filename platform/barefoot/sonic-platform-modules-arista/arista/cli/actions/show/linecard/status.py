
from . import registerAction
from ....args.show.linecard.status import statusParser
from ....show.card import ShowCardStatus

@registerAction(statusParser)
def doShowStatus(ctx, args):
   for linecard in ctx.linecards:
      ctx.show.addInventory(linecard)
   ctx.show.render(ShowCardStatus())
