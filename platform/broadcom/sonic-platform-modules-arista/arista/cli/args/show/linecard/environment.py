
from . import registerParser, showLinecardParser

@registerParser('environment', parent=showLinecardParser,
                help='Show environmental info')
def environmentParser(parser):
   pass
