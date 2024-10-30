from .. import registerParser
from . import showLinecardParser

@registerParser('reboot-cause', parent=showLinecardParser,
                help='Show reboot cause info')
def showRebootCauseParser(parser):
   parser.add_argument('-a', '--all', action='store_true',
      help='print reboot cause info for all attached chips')
   parser.add_argument('-H', '--history', action='store_true',
      help='print reboot causes history if it exists')
