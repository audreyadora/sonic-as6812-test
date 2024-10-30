
import errno
import os
import sys
import time

if sys.version_info.major == 2:
   PY_VERSION = 2
   def isinteger(value):
      return isinstance(value, (int, long))

   def monotonicRaw():
      return time.time()

   def makedirs(path, mode=0o777, exist_ok=False):
      try:
         os.makedirs(path, mode=mode)
      except OSError as e:
         if not exist_ok or e.errno != errno.EEXIST:
            raise

else:
   PY_VERSION = 3
   def isinteger(value):
      return isinstance(value, int)

   def monotonicRaw():
      return time.clock_gettime(time.CLOCK_MONOTONIC_RAW)

   makedirs = os.makedirs
