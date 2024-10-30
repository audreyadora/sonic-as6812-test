
from . import registerParser, showChassisParser

@registerParser('eeprom', parent=showChassisParser,
                help='Show chassis eeprom content')
def showChassisEepromParser(_parser):
   pass
