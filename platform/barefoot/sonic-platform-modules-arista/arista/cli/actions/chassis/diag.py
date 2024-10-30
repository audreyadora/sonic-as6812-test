
from __future__ import absolute_import, division, print_function

from .. import registerAction
from ..diag import doCommonDiagCli
from ...args.chassis.diag import diagParser

@registerAction(diagParser)
def doChassisDiag(ctx, args):
   doCommonDiagCli([ctx.platform.getChassis()], args)
