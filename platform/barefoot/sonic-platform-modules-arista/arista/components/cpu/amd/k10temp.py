
from ....core.component import Priority
from ....core.component.pci import PciComponent

from ....drivers.k10temp import K10TempKernelDriver

class K10Temp(PciComponent):
   DRIVER = K10TempKernelDriver
   PRIORITY = Priority.THERMAL
