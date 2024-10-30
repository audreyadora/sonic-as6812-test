
from . import registerParser, showFabricParser

@registerParser('environment', parent=showFabricParser,
                help='Show environmental info')
def environmentParser(parser):
   pass
