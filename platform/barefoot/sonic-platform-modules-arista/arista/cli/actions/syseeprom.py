
from __future__ import absolute_import, division, print_function

from . import registerAction
from ..args.syseeprom import syseepromParser
from ...core.platform import getSysEepromData

@registerAction(syseepromParser)
def doSysEeprom(ctx, args):
   for key, value in getSysEepromData().items():
      print('%s: %s' % (key, value))
