
from .. import registerAction
from ...args.fabric.power import powerParser
from ....core.log import getLogger

logging = getLogger(__name__)

@registerAction(powerParser)
def doSetup(ctx, args):
   power = args.state == 'on'
   for fabric in ctx.fabrics:
      try:
         fabric.powerOnIs(power)
      except Exception as e:  # pylint: disable=broad-except
         logging.error('Failed to power %s fabric %s: %s', args.state,
                       fabric, str(e))
