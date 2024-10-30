
from . import registerAction
from ....args.show.fabric.eeprom import showFabricEepromParser
from ....show.eeprom import ShowEeprom

@registerAction(showFabricEepromParser)
def doShowFabricEeprom(ctx, _args):
   for fabric in ctx.fabrics:
      ctx.show.addInventory(fabric.getEeprom(), SlotId=fabric.slot.slotId)
   ctx.show.render(ShowEeprom())
