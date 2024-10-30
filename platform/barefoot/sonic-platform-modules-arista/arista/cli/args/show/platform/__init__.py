
from ... import registerParser
from ...default import defaultPlatformParser
from ...show import showParser

@registerParser('platform', parent=showParser,
                help='Platform show commands')
def showPlatformParser(parser):
   defaultPlatformParser(parser)
