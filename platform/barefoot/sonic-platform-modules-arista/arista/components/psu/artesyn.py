from ...core.cooling import Airflow
from ...core.psu import PsuModel, PsuIdent


from . import PmbusPsu
from .ds460 import Ds460
from .helper import psuDescHelper, Position

class ArtesynPsu(PsuModel):
   MANUFACTURER = 'artesyn'
   MANUFACTURER_ALIASES = ['emerson'] # NOTE: acquired by Emerson
   PMBUS_ADDR = 0x58
   PMBUS_CLS = PmbusPsu

class DS495SPE(ArtesynPsu):
   CAPACITY = 500
   DESCRIPTION = psuDescHelper(
      sensors=[
         ('hotspot', Position.OTHER, 60, 111, 123),
         ('inlet', Position.INLET, 60, 80, 85),
         ('outlet', Position.OUTLET, 60, 80, 85),
      ],
   )
   IDENTIFIERS = [
      PsuIdent('DS495SPE-3-401 ', 'PWR-500AC-F', Airflow.EXHAUST),
      PsuIdent('DS495SPE-3-402 ', 'PWR-500AC-R', Airflow.INTAKE),
      PsuIdent('DS495SPE-3-404 ', 'PWR-500AC-R', Airflow.INTAKE),
      PsuIdent('DS495SPE-3-405 ', 'PWR-500AC-F', Airflow.EXHAUST),
   ]

class DS460(ArtesynPsu):
   CAPACITY = 460
   DESCRIPTION = psuDescHelper(
      sensors=[
         ('inlet', Position.INLET, 39, 60, 70),
         ('internal', Position.OTHER, 55, 80, 150),
      ],
   )
   IDENTIFIERS = [
      # NOTE: that first entry is a workaround for insufficient information exposed
      # through the pmbus MFR_*. Proper identification would require IPMI eeprom
      # parsing.
      PsuIdent('DS460', 'PWR-460AC-F', Airflow.EXHAUST),

      PsuIdent('DS460S-3    ', 'PWR-460AC-F', Airflow.EXHAUST),
      PsuIdent('DS460S-3-001', 'PWR-460AC-R', Airflow.INTAKE),
      PsuIdent('DS460S-3-002', 'PWR-460AC-F', Airflow.EXHAUST),
      PsuIdent('DS460S-3-003', 'PWR-460AC-R', Airflow.INTAKE),
   ]
   PMBUS_CLS = Ds460

class CSU500DP(ArtesynPsu):
   CAPACITY = 500
   DESCRIPTION = psuDescHelper(
      sensors=[
         ('inlet', Position.INLET, 60, 65, 69),
         ('secondary hotspot', Position.OTHER, 60, 105, 109),
         ('primary hotspot', Position.OTHER, 60, 104, 108),
      ],
   )
   IDENTIFIERS = [
      PsuIdent('CSU500DP-3    ', 'PWR-511-AC-RED', Airflow.EXHAUST),
      PsuIdent('CSU500DP-3-001', 'PWR-511-AC-BLUE', Airflow.INTAKE),
   ]

class Art700(ArtesynPsu):
   PMBUS_ADDR = 0x40
   DRIVER = 'dps800'
   CAPACITY = 3000
   DUAL_INPUT = True
   DESCRIPTION = psuDescHelper(
      sensors=[
         ('inlet', Position.INLET, 60, 65, 70),
         ('primary hotspot', Position.OTHER, 70, 95, 100),
         ('secondary hotspot', Position.OTHER, 70, 125, 130),
      ],
      maxRpm=29000,
   )
   IDENTIFIERS = [
      PsuIdent('700-015522-0000', 'PWR-D4-3041-AC-BLUE', Airflow.INTAKE),
   ]
