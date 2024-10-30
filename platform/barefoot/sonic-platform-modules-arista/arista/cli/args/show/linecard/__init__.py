
from ... import registerParser
from ...linecard import linecardParser
from ...show import showParser

@registerParser('linecard', parent=showParser,
                help='Linecard show commands')
def showLinecardParser(parser):
   linecardParser(parser)
