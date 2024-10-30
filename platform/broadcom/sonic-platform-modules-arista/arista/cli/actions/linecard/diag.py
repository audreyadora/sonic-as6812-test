
from __future__ import absolute_import, division, print_function

from .. import registerAction
from ..diag import doCommonDiagCli
from ...args.linecard.diag import diagParser

@registerAction(diagParser)
def doLinecardDiag(ctx, args):
   doCommonDiagCli(ctx.linecards, args)
