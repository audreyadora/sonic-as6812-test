
from __future__ import absolute_import, division, print_function

import json

from ...core.diag import DiagContext
from ...libs.pyshell import pyshell

def doCommonDiagCli(components, args):
   diagCtx = DiagContext(
      performIo=not args.noIo,
      recursive=args.recursive,
      safe=args.safe,
   )
   diagInfo = []

   for component in components:
      if args.recursive:
         diagInfo.append(component.genDiag(diagCtx))
      else:
         for c in component.iterComponents():
            diagInfo.append(c.genDiag(diagCtx))

   if args.pyshell:
      pyshell()
   else:
      ident = 3 if args.pretty else None
      print(json.dumps(diagInfo, indent=ident))
