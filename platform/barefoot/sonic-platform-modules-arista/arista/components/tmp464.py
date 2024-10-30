
from ..drivers.tmp468 import Tmp464KernelDriver

from .tmp468 import Tmp468

class Tmp464(Tmp468):
   DRIVER = Tmp464KernelDriver
