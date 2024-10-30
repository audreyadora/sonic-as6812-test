
from __future__ import absolute_import, division, print_function

from .. import registerParser
from . import linecardParser

from ....core.provision import ProvisionMode

@registerParser('provision', parent=linecardParser)
def provisionParser(parser):
   parser.add_argument('--set', type=lambda mode: ProvisionMode[mode.upper()],
                       choices=list(ProvisionMode), help='set the provision mode')
