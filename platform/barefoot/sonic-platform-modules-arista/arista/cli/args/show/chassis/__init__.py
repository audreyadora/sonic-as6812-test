
from .. import registerParser, showParser
from ...chassis import chassisParser

@registerParser('chassis', parent=showParser,
                help='Chassis show commands')
def showChassisParser(parser):
   chassisParser(parser)
