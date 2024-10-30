
from ..cpld import SysCpld, SysCpldCommonRegistersV2
from ..scd import ScdReloadCauseRegisters

class LorikeetCpldRegisters(SysCpldCommonRegistersV2):
   pass

class LorikeetSysCpld(SysCpld):
   REGISTER_CLS = LorikeetCpldRegisters

class LorikeetPrimeScdReloadCauseRegisters(ScdReloadCauseRegisters):
   pass
