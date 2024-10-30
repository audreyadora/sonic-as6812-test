import os
import time

from ..core.log import getLogger
from ..core.utils import inSimulation
from ..core.types import PciAddr
from ..libs.wait import waitFor

logging = getLogger(__name__)

def pciRescan():
   logging.info('triggering kernel pci rescan')
   with open('/sys/bus/pci/rescan', 'w') as f:
      f.write('1')

def readSecondaryBus(pciAddr):
   if isinstance(pciAddr, PciAddr):
      pciAddr = str(pciAddr)

   '''Find secondary bus of a device with its PCI address.'''
   if inSimulation():
      bus = pciAddr.split(":")[1]
      return int(bus) + 1

   devPath = '/sys/bus/pci/devices/%s/secondary_bus_number' % pciAddr
   waitFor(lambda: os.path.exists(devPath), "Unable to get %s secondary bus" % pciAddr,
           timeout=60, interval=100)

   def readBus():
      with open(devPath) as f:
          secondaryBus = int(f.readline())
      return secondaryBus

   def readAndCompareBus():
      # There is a bug where we try to read secondary bus number but kernel doesn't
      # completely write into the file. Double read to make sure thing is right.
      secondaryBus = readBus()
      time.sleep(0.1)
      return secondaryBus == readBus()

   waitFor(readAndCompareBus, description="Read and compare secondary bus fails")
   return readBus()

class PciIds():
   def __init__(self):
      self.vendors = {}
      self.classes = {}

      self.cvendor = None
      self.cdevice = None
      self.isClass = False

   def processLine(self, line):
      if line.startswith('C '):
         self.isClass = True
         self.cvendor = None
         self.cdevice = None
      elif line.startswith('\t\t'):
         if self.isClass:
            pass
         else:
            data = line.split('  ', 1)
            svendor, sdevice = (int(d, 16) for d in data[0].split())
            self.cdevice['subsystems'][(svendor, sdevice)] = data[1]
      elif line.startswith('\t'):
         if self.isClass:
            pass
         else:
            data = line.split('  ', 1)
            self.cdevice = {
               'id': int(data[0], 16),
               'name': data[1],
               'subsystems': {}
            }
            self.cvendor['devices'][self.cdevice['id']] = self.cdevice
      else:
         self.isClass = False
         data = line.split('  ', 1)
         self.cvendor = {
            'id': int(data[0], 16),
            'name': data[1],
            'devices': {}
         }
         self.vendors[self.cvendor['id']] = self.cvendor

   def load(self, path='/usr/share/misc/pci.ids'):
      if not os.path.exists(path):
         return
      with open(path, encoding='utf8') as f:
         for line in f.readlines():
            line = line.rstrip()
            if not line or line.startswith('#'):
               continue
            try:
               self.processLine(line)
            except:
               raise
      self.cvendor = None
      self.cdevice = None

   def deviceName(self, vendor, device, svendor=None, sdevice=None):
      suffix = ' [%04x:%04x]' % (vendor, device)
      v = self.vendors.get(vendor)
      if v is None:
         return '(Vendor) (Device)%s' % suffix
      d = v['devices'].get(device)
      if d is None:
         return '%s (Device)%s' % (v['name'], suffix)
      devname = d['name']
      if svendor is not None and sdevice is not None:
         suffix += '(%04x:%04x)' % (svendor, sdevice)
         s = d['subsystems'].get((svendor, sdevice))
         if s is not None:
            devname = s
      return '%s %s%s' % (v['name'], devname, suffix)

