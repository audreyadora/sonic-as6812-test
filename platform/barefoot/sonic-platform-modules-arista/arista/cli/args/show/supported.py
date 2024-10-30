
from . import registerParser, showParser

@registerParser('supported', parent=showParser, help='show supported platforms')
def supportedParser(parser):
   pass
