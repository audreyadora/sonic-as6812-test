from __future__ import absolute_import, division, print_function

class DiagContext(object):
   def __init__(self, performIo=True, recursive=False, safe=False):
      self.performIo = performIo
      self.recursive = recursive
      self.safe = safe
      self.inventories = set() # set of visited inventories
