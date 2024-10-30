
from ..core.component import Priority
from ..core.component.i2c import I2cComponent

from ..drivers.ds125br import Ds125BrDevDriver

class Ds125Br(I2cComponent):
   DRIVER = Ds125BrDevDriver
   PRIORITY = Priority.DEFAULT
