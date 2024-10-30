
from .. import registerAction
from ...fabric import doFabric
from ....args.show.fabric import showFabricParser

@registerAction(showFabricParser)
def doShowFabric(ctx, args):
   doFabric(ctx, args)
