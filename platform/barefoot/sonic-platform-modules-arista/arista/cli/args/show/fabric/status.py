
from . import registerParser, showFabricParser

@registerParser('status', parent=showFabricParser,
                help='Show fabric status')
def statusParser(parser):
   pass
