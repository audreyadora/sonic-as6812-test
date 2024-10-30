
from . import registerAction
from ....args.show.fabric.environment import environmentParser
from ....show.environment import ShowEnvironment

@registerAction(environmentParser)
def doShowEnvironment(ctx, args):
   for fabric in ctx.fabrics:
      ctx.show.addInventory(fabric.getInventory())
   ctx.show.render(ShowEnvironment())
