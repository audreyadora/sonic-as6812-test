
from . import registerParser, showFabricParser

@registerParser('eeprom', parent=showFabricParser,
                help='Show fabric eeprom content')
def showFabricEepromParser(_parser):
   pass
