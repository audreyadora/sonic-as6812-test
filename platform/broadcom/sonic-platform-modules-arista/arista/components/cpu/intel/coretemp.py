
from ....core.component import Priority
from ....core.component.pci import PciComponent

from ....drivers.coretemp import CoretempKernelDriver

class Coretemp(PciComponent):
   DRIVER = CoretempKernelDriver
   PRIORITY = Priority.THERMAL
