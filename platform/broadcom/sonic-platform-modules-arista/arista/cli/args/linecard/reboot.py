from .. import registerParser
from . import linecardParser

@registerParser('reboot', parent=linecardParser)
def rebootParser(parser):
   parser.add_argument('--mode', default='soft', choices=['soft', 'hard'],
      help='reset switch ASIC if in hard mode')
