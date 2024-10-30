
from ....core.component.i2c import I2cComponent
from ....drivers.sbtsi import SbTsiUserDriver

class SbTsi(I2cComponent):
   DRIVER = SbTsiUserDriver
