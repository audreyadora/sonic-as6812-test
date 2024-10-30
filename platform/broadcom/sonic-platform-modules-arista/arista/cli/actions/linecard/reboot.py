
from .. import registerAction
from ...args.linecard.reboot import rebootParser
from ....core.log import getLogger
from ....core.reboot import LinecardRebootManager

logging = getLogger(__name__)

@registerAction(rebootParser)
def doReboot(ctx, args):
   chassis = ctx.platform.getChassis()
   lrm = LinecardRebootManager(chassis, ctx.linecards)
   lrm.rebootLinecards(args.mode)
