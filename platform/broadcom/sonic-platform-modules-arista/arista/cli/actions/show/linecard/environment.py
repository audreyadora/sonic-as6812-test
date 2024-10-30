
from . import registerAction
from ....args.show.linecard.environment import environmentParser
from ....show.environment import ShowEnvironment

@registerAction(environmentParser)
def doShowEnvironment(ctx, args):
   for linecard in ctx.linecards:
      ctx.show.addInventory(linecard.getInventory())
   ctx.show.render(ShowEnvironment())
