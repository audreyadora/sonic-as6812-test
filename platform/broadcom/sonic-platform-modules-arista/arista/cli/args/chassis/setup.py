
from __future__ import absolute_import, division, print_function

from .. import registerParser
from . import chassisParser

@registerParser('setup', parent=chassisParser,
                help='setup drivers for this platform')
def setupParser(parser):
   pass
