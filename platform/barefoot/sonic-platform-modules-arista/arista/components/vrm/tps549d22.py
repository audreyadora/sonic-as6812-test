
from ...drivers.vrm.tps549d22 import Tps549D22UserDriver

from . import Vrm

class Tps549D22(Vrm):
   DRIVER = Tps549D22UserDriver
