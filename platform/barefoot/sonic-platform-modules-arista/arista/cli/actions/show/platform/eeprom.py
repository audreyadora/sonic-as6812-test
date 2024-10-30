
from . import registerAction
from ....args.show.platform.eeprom import showPlatformEepromParser
from ....show.eeprom import ShowEeprom

@registerAction(showPlatformEepromParser)
def doShowPlatformEeprom(ctx, _args):
   ctx.show.addInventory(ctx.platform.getEeprom())
   ctx.show.render(ShowEeprom())
