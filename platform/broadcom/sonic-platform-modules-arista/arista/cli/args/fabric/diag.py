from __future__ import absolute_import, division, print_function

from .. import registerParser
from ..diag import addDiagCommonParser
from ..fabric import fabricParser

@registerParser('diag', parent=fabricParser,
                help='dump diag information for fabrics')
def diagParser(parser):
   addDiagCommonParser(parser)
