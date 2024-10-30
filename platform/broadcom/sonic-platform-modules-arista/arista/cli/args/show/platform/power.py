
from . import registerParser, showPlatformParser

@registerParser('power', parent=showPlatformParser,
                help='Show power info')
def powerParser(parser):
   pass
