
import importlib
import pkgutil

def walk_packages(path=None, prefix='', onerror=None):
   """Implementation from https://github.com/python/cpython/pull/11956"""
   def seen(p, m={}): # pylint: disable=dangerous-default-value
      if p in m:
         return True
      m[p] = True
      return False

   for info in pkgutil.iter_modules(path, prefix):
      yield info

      if info.ispkg:
         # loader = info.module_finder.find_module('arista.cli.args.' + info.name)
         loader = info.module_finder.find_module(info.name)
         try:
            # module = loader.load_module('arista.cli.args.' + info.name)
            module = loader.load_module(info.name)
         except ImportError:
            if onerror is not None:
               onerror(info.name)
         except Exception: # pylint: disable=broad-except
            if onerror is not None:
               onerror(info.name)
            else:
               raise
         else:
            path = module.__path__

            # don't traverse path items we've seen before
            path = [p for p in path if not seen(p)]

            yield from walk_packages(path, info.name + '.', onerror)

def importSubmodules(package, prefix=None, recursive=True):
   if isinstance(package, str):
      prefix = package + '.'
      package = importlib.import_module(package)
   else:
      prefix = package.__module__

   modules = {}
   for info in walk_packages(package.__path__, prefix=prefix):
      fullName = info.name
      modules[fullName] = importlib.import_module(fullName)
      if recursive and info.ispkg:
         modules.update(importSubmodules(fullName, fullName + '.'))

   return modules
