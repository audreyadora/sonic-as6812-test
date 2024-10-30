
from ..core.driver.kernel import KernelDriver

class RavenFanKernelDriver(KernelDriver):
   MODULE = 'raven-fan-driver'
   PATH = '/sys/devices/platform/sb800-fans'
