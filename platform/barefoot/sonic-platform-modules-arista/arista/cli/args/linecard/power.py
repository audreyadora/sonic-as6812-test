
from .. import registerParser
from . import linecardParser

@registerParser('power', parent=linecardParser)
def powerParser(parser):
   parser.add_argument('state', choices=['on', 'off'],
      help="change the power state of the linecard")
   parser.add_argument('--lcpu', action='store_true', default=None,
      help="activate linecard cpu if any")
   parser.add_argument('--powerCycleIfOn', action='store_true',
      help='power cycle the linecard if already on')
