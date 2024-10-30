
from .. import registerAction
from ...args.linecard.power import powerParser
from ....core.config import Config
from ....core.log import getLogger
from ....core.linecard import LCpuCtx

logging = getLogger(__name__)

@registerAction(powerParser)
def doPower(ctx, args):
   power = args.state == 'on'

   lcpuCtx = None
   if args.lcpu is not None or Config().linecard_cpu_enable:
      lcpuCtx = LCpuCtx()

   for linecard in ctx.linecards:
      try:
         if lcpuCtx and not linecard.hasCpuModule():
            logging.info('%s has no LCPU module, skipping...', linecard)
            continue

         if linecard.poweredOn() and args.powerCycleIfOn and power:
            linecard.powerOnIs(False, lcpuCtx=lcpuCtx)
         linecard.powerOnIs(power, lcpuCtx=lcpuCtx)
      except Exception as e: # pylint: disable=broad-except
         logging.error('Failed to power %s linecard %s: %s', args.state,
                       linecard, str(e))
