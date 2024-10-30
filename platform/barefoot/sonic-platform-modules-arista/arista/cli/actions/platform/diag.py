
from __future__ import absolute_import, division, print_function

from .. import registerAction
from ..diag import doCommonDiagCli
from ...args.platform.diag import diagParser

@registerAction(diagParser)
def doPlatformDiag(ctx, args):
   doCommonDiagCli([ctx.platform], args)
