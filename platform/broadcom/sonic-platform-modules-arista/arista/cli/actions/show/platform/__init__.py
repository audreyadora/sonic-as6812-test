
from .. import registerAction
from ...platform import doPlatform
from ....args.show.platform import showPlatformParser

@registerAction(showPlatformParser)
def doShowPlatform(ctx, args):
   doPlatform(ctx, args)
   ctx.show.addPlatform(ctx.platform)
