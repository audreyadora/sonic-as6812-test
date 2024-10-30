
from ...drivers.vrm.sic450 import Sic450UserDriver

from . import Vrm

class Sic450(Vrm):
   DRIVER = Sic450UserDriver
