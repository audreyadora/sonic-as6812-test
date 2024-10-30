
from collections import OrderedDict

try:
   # pylint: disable=unused-import
   from ..__version__ import __VERSION__, __DATE__
except ImportError:
   __VERSION__ = "unknown"
   __DATE__ = "unknown"

def getVersionInfo():
   return OrderedDict([
      ('version', __VERSION__),
      ('date', __DATE__),
   ])

