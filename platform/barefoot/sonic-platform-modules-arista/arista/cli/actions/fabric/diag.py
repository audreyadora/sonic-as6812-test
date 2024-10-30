
from __future__ import absolute_import, division, print_function

from .. import registerAction
from ..diag import doCommonDiagCli
from ...args.fabric.diag import diagParser

@registerAction(diagParser)
def doFabricDiag(ctx, args):
   doCommonDiagCli(ctx.fabrics, args)
