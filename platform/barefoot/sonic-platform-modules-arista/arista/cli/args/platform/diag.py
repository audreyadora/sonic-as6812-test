
from __future__ import absolute_import, division, print_function

from .. import registerParser
from ..diag import addDiagCommonParser
from ..platform import platformParser

@registerParser('diag', parent=platformParser,
                help='dump diag information for the platform')
def diagParser(parser):
   addDiagCommonParser(parser)
