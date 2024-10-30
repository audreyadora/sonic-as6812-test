
from ... import registerParser
from ...fabric import fabricParser
from ...show import showParser

@registerParser('fabric', parent=showParser,
                help='Fabric show commands')
def showFabricParser(parser):
   fabricParser(parser)
