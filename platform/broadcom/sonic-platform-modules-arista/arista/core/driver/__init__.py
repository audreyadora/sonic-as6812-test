
import os
import subprocess

from .. import utils
from ..utils import FileWaiter, inDebug, inSimulation
from ..log import getLogger

logging = getLogger(__name__)

def modprobe(name, args=None):
   logging.debug('loading module %s', name)
   if args is None:
      args = []
   args = ['modprobe', name.replace('-', '_')] + args
   if inDebug():
      args += ['dyndbg=+pf']
   if inSimulation():
      logging.debug('exec: %s', ' '.join(args))
   else:
      subprocess.check_call(args)

def deviceListForModule(name):
   devices = []
   moduleDriversPath = '/sys/module/%s/drivers/' % name.replace('-', '_')

   if not os.path.exists(moduleDriversPath):
      return []

   for drv in os.listdir(moduleDriversPath):
      moduleDevicesPath = os.path.join(moduleDriversPath, drv)
      for device in os.listdir(moduleDevicesPath):
         deviceLinkPath = os.path.join(moduleDevicesPath, device)
         try:
            deviceLinkValue = os.readlink(deviceLinkPath)
            deviceAbsPath = os.path.abspath(os.path.join(moduleDevicesPath,
                                                         deviceLinkValue))
            if deviceAbsPath.startswith('/sys/devices'):
               devices += [deviceAbsPath]
         except OSError:
            continue

   return devices

def rmmod(name):
   logging.debug('unloading module %s', name)
   args = ['modprobe', '-r', name.replace('-', '_')]
   if inSimulation():
      logging.debug('exec: %s', ' '.join(args))
   else:
      subprocess.check_call(args)

def isModuleLoaded(name):
   if inSimulation():
      return False

   with open('/proc/modules') as f:
      start = '%s ' % name.replace('-', '_')
      for line in f.readlines():
         if line.startswith(start):
            return True
   return False

class Driver(object):
   def __init__(self, **kwargs):
      self.__dict__.update(kwargs)

   def setup(self):
      pass

   def finish(self):
      pass

   def clean(self):
      pass

   def refresh(self):
      pass

   def resetIn(self):
      pass

   def resetOut(self):
      pass

   def __diag__(self, ctx): # pylint: disable=unused-argument
      return {}

   def __try_diag__(self, ctx):
      try:
         return self.__diag__(ctx)
      except Exception: # pylint: disable=broad-except
         if not ctx.safe:
            raise
         return {}

   def genDiag(self, ctx):
      return {
         "version": 1,
         "name": self.__class__.__name__,
         "data": self.__try_diag__(ctx),
      }

   def __str__(self):
      kwargs = ['%s=%s' % (k, v) for k, v in self.__dict__.items()]
      return '%s(%s)' % (self.__class__.__name__, ', '.join(kwargs))
