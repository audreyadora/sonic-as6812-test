
from . import registerAction
from ....args.show.linecard.eeprom import showLinecardEepromParser
from ....show.eeprom import ShowEeprom

@registerAction(showLinecardEepromParser)
def doShowLinecardEeprom(ctx, _args):
   for linecard in ctx.linecards:
      ctx.show.addInventory(linecard.getEeprom(), SlotId=linecard.slot.slotId)
   ctx.show.render(ShowEeprom())
