
from .. import registerParser
from . import showChassisParser

@registerParser('summary', parent=showChassisParser,
                help='Show information about the chassis')
def chassisSummaryParser(parser):
   pass
