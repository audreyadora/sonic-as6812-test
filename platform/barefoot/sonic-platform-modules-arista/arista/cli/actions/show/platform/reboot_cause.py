
from . import registerAction
from ....args.show.platform.reboot_cause import rebootCauseParser
from ....show.reboot_cause import ShowPlatformRebootCause

@registerAction(rebootCauseParser)
def doShowEnvironment(ctx, args):
   ctx.show.render(ShowPlatformRebootCause())
