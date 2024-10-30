from ...core.component import Priority
from ...core.component.component import Component

from ...drivers.raven import RavenFanKernelDriver

class RavenFanComplex(Component):
   PRIORITY = Priority.THERMAL
   DRIVER = RavenFanKernelDriver
