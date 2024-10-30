from .. import registerAction
from ...args.linecard.reboot_cause import rebootCauseParser
from ....core import utils
from ....core.config import Config
from ....core.cause import getLinecardReloadCauseManager

@registerAction(rebootCauseParser)
def doRebootCause(ctx, args):
   if utils.inSimulation():
      return

   for linecard in ctx.linecards:
      try:
         lock_file = Config().linecard_lock_file_pattern.format(linecard.getSlotId())
         with utils.FileLock(lock_file):
            getLinecardReloadCauseManager(linecard, read=args.process)
      except Exception: # pylint: disable=broad-except
         print(f'Failed to read reboot-cause information from linecard {linecard}')
