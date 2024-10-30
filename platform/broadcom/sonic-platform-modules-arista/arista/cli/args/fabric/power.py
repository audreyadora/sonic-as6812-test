
from .. import registerParser
from . import fabricParser

@registerParser('power', parent=fabricParser)
def powerParser(parser):
   parser.add_argument('state', choices=['on', 'off'],
      help="change the power state of the fabric")
