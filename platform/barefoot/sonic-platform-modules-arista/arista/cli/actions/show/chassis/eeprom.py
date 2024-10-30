
from . import registerAction
from ....args.show.chassis.eeprom import showChassisEepromParser
from ....show.eeprom import ShowEeprom

@registerAction(showChassisEepromParser)
def doShowChassisEeprom(ctx, _args):
   ctx.show.addInventory(ctx.chassis.getEeprom())
   ctx.show.render(ShowEeprom())
