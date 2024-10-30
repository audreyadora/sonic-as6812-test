
import time

def tryGet(func, default=None):
   try:
      return func()
   except Exception: # pylint: disable=broad-except
      return default

def retryGet(func, default=None, retries=1, wait=1., before=False):
   for i in range(retries + 1):
      if before and wait:
         time.sleep(wait)

      try:
         return func()
      except Exception: # pylint: disable=broad-except
         pass

      if not before and wait and i < retries - 1:
         time.sleep(wait)

   return default
