
import contextlib
import time

from ..core.log import getLogger

logging = getLogger(__name__)

@contextlib.contextmanager
def timeit(message):
   begin = time.time()
   try:
      yield
   finally:
      end = time.time()
      logging.debug('%s (took %s seconds)', message, end - begin)
