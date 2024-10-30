
from .. import registerAction
from ...linecard import doLinecard
from ....args.show.linecard import showLinecardParser

@registerAction(showLinecardParser)
def doShowLinecard(ctx, args):
   doLinecard(ctx, args)
