
from . import registerParser, showLinecardParser

@registerParser('eeprom', parent=showLinecardParser,
                help='Show linecard eeprom content')
def showLinecardEepromParser(_parser):
   pass
