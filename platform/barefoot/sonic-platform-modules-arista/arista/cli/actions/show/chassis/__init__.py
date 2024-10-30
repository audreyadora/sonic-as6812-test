
from .. import registerAction
from ...chassis import doChassis
from ....args.show.chassis import showChassisParser

@registerAction(showChassisParser)
def doShowChassis(ctx, args):
   doChassis(ctx, args)
