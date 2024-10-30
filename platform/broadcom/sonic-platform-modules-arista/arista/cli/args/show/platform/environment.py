
from . import registerParser, showPlatformParser

@registerParser('environment', parent=showPlatformParser,
                help='Show environmental info')
def environmentParser(parser):
   pass
