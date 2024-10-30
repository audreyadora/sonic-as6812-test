
from . import registerAction
from ....args.show.platform.environment import environmentParser
from ....show.environment import ShowEnvironment

@registerAction(environmentParser)
def doShowEnvironment(ctx, args):
   ctx.show.addInventory(ctx.platform.getInventory())
   ctx.show.render(ShowEnvironment())
