
from __future__ import absolute_import, division, print_function

from .. import registerParser
from ..default import defaultPlatformParser

@registerParser('platform', parent=defaultPlatformParser,
                help='Platform related features')
def platformParser(parser):
   pass
