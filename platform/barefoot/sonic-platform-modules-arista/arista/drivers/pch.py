
from ..core.driver.kernel.pci import PciKernelDriver

class PchTempKernelDriver(PciKernelDriver):
   MODULE = 'intel_pch_thermal'
   PASSIVE = True

   def getHwmonPath(self):
      # NOTE: there is no direct link from device to hwmon folder
      #       path expectation is therefore hardcoded
      return '/sys/devices/virtual/thermal/thermal_zone0/hwmon0'
