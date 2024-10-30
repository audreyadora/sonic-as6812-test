
from ...drivers.ds460 import Ds460KernelDriver

from . import PmbusPsu

class Ds460(PmbusPsu):
   DRIVER = Ds460KernelDriver
