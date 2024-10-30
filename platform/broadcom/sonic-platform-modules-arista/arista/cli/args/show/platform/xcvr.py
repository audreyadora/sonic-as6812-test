
from . import registerParser, showPlatformParser

@registerParser('xcvr', parent=showPlatformParser,
                help='Show transceiver info')
def xcvrParser(parser):
   pass
