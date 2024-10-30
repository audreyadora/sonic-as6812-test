
from ..cpld import SysCpld
from ..scd import ScdReloadCauseRegisters

from .shearwater import ShearwaterSysCpldRegisters

class RedstartSysCpld(SysCpld):
   REGISTER_CLS = ShearwaterSysCpldRegisters

class RedstartReloadCauseRegisters(ScdReloadCauseRegisters):
   pass
