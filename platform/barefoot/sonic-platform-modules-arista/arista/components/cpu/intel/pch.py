
from ....core.component import Priority
from ....core.component.pci import PciComponent

from ....drivers.pch import PchTempKernelDriver

class PchTemp(PciComponent):
   DRIVER = PchTempKernelDriver
   PRIORITY = Priority.THERMAL
