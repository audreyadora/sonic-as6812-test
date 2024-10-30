
from . import registerAction
from ....args.show.platform.xcvr import xcvrParser
from ....show.xcvr import ShowXcvr

@registerAction(xcvrParser)
def doShowXcvr(ctx, args):
   ctx.show.addInventory(ctx.platform.getInventory())
   ctx.show.render(ShowXcvr())
