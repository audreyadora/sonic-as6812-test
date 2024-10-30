
from __future__ import absolute_import, division, print_function

from . import registerParser
from .common import addPriorityArgs
from .default import defaultPlatformParser

@registerParser('setup', parent=defaultPlatformParser,
                help='setup drivers for this platform')
def setupParser(parser):
   parser.add_argument('-r', '--reset', action='store_true',
      help='put devices out of reset after init')
   parser.add_argument('-d', '--debug', action='store_true',
      help='enable debug features for the drivers')
   parser.add_argument('-b', '--background', action='store_true',
      help='initialize slow, non-critical drivers in background')
   addPriorityArgs(parser)
