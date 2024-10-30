import copy

from .inventory import Inventory

_TEMPLATE_INVENTORY = Inventory()

class LazyInventory(Inventory):
   def __init__(self):
      pass

   def __getattr__(self, key):
      if not hasattr(_TEMPLATE_INVENTORY, key):
         raise AttributeError

      value = copy.deepcopy(getattr(_TEMPLATE_INVENTORY, key))
      setattr(self, key, value)
      return value

class MetaInventory(object):
   def __init__(self, invs=None):
      # NOTE: invs could have been an iterator but it can only be used one
      #       for dynamic inventory list, use a function that returns
      #       inventories.
      self.invs = list(invs) if invs is not None else []

   def __getattr__(self, key):
      func = getattr(Inventory, key)

      def callbackCol():
         data = None
         count = 0
         for inv in self.invs:
            res = func(inv)
            if data is None:
               data = type(res)()
            if isinstance(res, dict):
               data.update(res)
            elif isinstance(res, list):
               data.extend(res)
            elif isinstance(res, int):
               data += res
            else:
               raise ValueError('Unknown type to process')
            count += 1
         if count == 0:
            return copy.deepcopy(getattr(_TEMPLATE_INVENTORY, key)())
         return data

      def callbackItem(*args):
         for inv in self.invs:
            try:
               res = func(inv, *args)
            except KeyError: # NOTE: could be enhanced via a has* call
               continue
            return res
         raise KeyError(*args)

      def callback(*args):
         if args:
            return callbackItem(*args)
         return callbackCol()

      return callback
