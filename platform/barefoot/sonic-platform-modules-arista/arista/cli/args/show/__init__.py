
from .. import registerParser
from ..default import defaultPlatformParser

@registerParser('show', parent=defaultPlatformParser,
                help='Show commands')
def showParser(parser):
   parser.add_argument('-j', '--json', action='store_true',
      help='output library information in json format')
   parser.add_argument('-p', '--pretty', action='store_true',
      help='generate a pretty output when applicable')
