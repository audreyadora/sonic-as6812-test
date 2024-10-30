
from ..core.driver.kernel import KernelDriver

class CoretempKernelDriver(KernelDriver):
   MODULE = 'coretemp'
   PATH = "/sys/devices/platform/coretemp.0"
   PASSIVE = True
