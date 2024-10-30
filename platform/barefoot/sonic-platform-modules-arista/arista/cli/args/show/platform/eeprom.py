
from . import registerParser, showPlatformParser

@registerParser('eeprom', parent=showPlatformParser,
                help='Show platform eeprom content')
def showPlatformEepromParser(_parser):
   pass
