
from __future__ import absolute_import, division, print_function

from .. import registerAction
from ...exception import ActionError
from ...args.platform import platformParser

@registerAction(platformParser)
def doPlatform(ctx, args):
   pass
