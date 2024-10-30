from .. import registerAction
from ....args.show.linecard.reboot_cause import showRebootCauseParser
from ....show.reboot_cause import ShowLinecardRebootCause

# pylint: disable=unused-argument

@registerAction(showRebootCauseParser)
def doRebootCause(ctx, args):
   for linecard in ctx.linecards:
      ctx.show.addInventory(linecard)
   ctx.show.render(ShowLinecardRebootCause())
