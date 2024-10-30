
from ..libs.python import PY_VERSION

class DiagInfo(object):
   def __init__(self, func, name, io, default, fmt, diag):
      self.func = func
      self.name = name
      self.io = io
      self.default = default
      self.fmt = fmt
      self.diag = diag

def idfmt(value):
   return value

def diagmethod(name, io=False, default=None, fmt=idfmt, diag=False):
   def wrapper(func):
      func_name = func.__name__ if PY_VERSION > 2 else func.func_name
      func.diag = DiagInfo(func_name, name, io, default, fmt, diag)
      return func
   return wrapper

def diagcls(cls):
   infos = []
   for method in cls.__dict__.values():
      info = getattr(method, 'diag', None)
      if info is None:
         continue
      infos.append(info)
   cls._DIAG_INFO = infos # pylint: disable=protected-access
   return cls

class InventoryInterface(object):

   _DIAG_INFO = None

   def __diag_post__(self, ctx, data):
      return data

   def __diag__(self, ctx):
      res = {}
      if not self._DIAG_INFO:
         return res

      for info in self._DIAG_INFO or []:
         if info.io and not ctx.performIo:
            value = info.default
         else:
            try:
               value = info.fmt(getattr(self, info.func)())
               if info.diag and value is not None:
                  if isinstance(value, list):
                     value = [v.__diag__(ctx) for v in value]
                  else:
                     value = value.__diag__(ctx)
            except Exception: # pylint: disable=broad-except
               value = info.default
         res[info.name] = value
      return self.__diag_post__(ctx, res)

   def genDiag(self, ctx):
      desc = getattr(self, 'desc', None)
      return {
         "version": 2,
         "classes": [c.__name__ for c in self.__class__.__mro__[:-1]],
         "name": self.__class__.__name__,
         "desc": desc.__diag__(ctx) if desc else {},
         "data": self.__diag__(ctx),
      }
