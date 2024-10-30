
from . import registerParser, showLinecardParser

@registerParser('status', parent=showLinecardParser,
                help='Show linecard status')
def statusParser(parser):
   pass
