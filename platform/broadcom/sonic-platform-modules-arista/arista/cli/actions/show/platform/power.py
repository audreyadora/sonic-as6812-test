
from . import registerAction
from ....args.show.platform.power import powerParser
from ....show.power import ShowPower

@registerAction(powerParser)
def doShowPower(ctx, args):
   ctx.show.render(ShowPower())
