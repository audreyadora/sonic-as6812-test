
from .. import registerAction
from ...exception import ActionError
from ...args.show import showParser

from ...show import Show

@registerAction(showParser)
def doShow(ctx, args):
   outputFormat = Show.TXT
   if args.json:
      outputFormat = Show.JSON

   setattr(ctx, 'show', Show(outputFormat=outputFormat, args=args))
