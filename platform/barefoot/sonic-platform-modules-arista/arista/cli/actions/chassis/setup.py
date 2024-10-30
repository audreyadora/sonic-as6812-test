
from __future__ import absolute_import, division, print_function

from .. import registerAction
from ...args.chassis.setup import setupParser

@registerAction(setupParser)
def doSetup(ctx, args):
   print('TODO: setup for', ctx.chassis)
