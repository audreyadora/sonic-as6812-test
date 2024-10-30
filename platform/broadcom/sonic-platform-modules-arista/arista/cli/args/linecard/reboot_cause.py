from .. import registerParser
from . import linecardParser

@registerParser('reboot-cause', parent=linecardParser)
def rebootCauseParser(parser):
   parser.add_argument('--process', action='store_true',
      help='process last reboot cause and generate report (do not use)')
