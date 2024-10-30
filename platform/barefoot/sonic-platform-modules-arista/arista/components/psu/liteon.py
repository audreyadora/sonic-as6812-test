from ...core.cooling import Airflow
from ...core.psu import PsuModel, PsuIdent

from . import PmbusPsu
from .helper import psuDescHelper, Position

class LiteonPsu(PsuModel):
   MANUFACTURER = 'liteon power'
   PMBUS_ADDR = 0x58

   PMBUS_CLS = PmbusPsu

class PS2102(LiteonPsu):
   DRIVER = 'dps800'
   CAPACITY = 1000
   IDENTIFIERS = [
      PsuIdent('PS-2102-1A ', 'PWR-1011-AC-RED',  Airflow.EXHAUST),
      PsuIdent('DD-2102-1A ', 'PWR-1011-DC-RED',  Airflow.EXHAUST),
      PsuIdent('PS-2102-1AR', 'PWR-1011-AC-BLUE', Airflow.INTAKE),
      PsuIdent('DD-2102-1AR', 'PWR-1011-DC-BLUE', Airflow.INTAKE),
   ]
   DESCRIPTION = psuDescHelper(
      sensors=[
         ('inlet', Position.OTHER, 60, 75, 85),
         ('secondary hotspot', Position.OTHER, 70, 105, 110),
         ('primary hotspot', Position.OTHER, 70, 95, 100),
      ],
      maxRpm=25500,
   )

class PS2242(LiteonPsu):
   DRIVER = 'dps800'
   CAPACITY = 2400
   IDENTIFIERS = [
      PsuIdent('PS-2242-3A ', 'PWR-2411-AC-RED',  Airflow.EXHAUST),
      PsuIdent('DD-2242-3A ', 'PWR-2411-DC-RED',  Airflow.EXHAUST),
      PsuIdent('PS-2242-3AR', 'PWR-2411-AC-BLUE', Airflow.INTAKE),
      PsuIdent('DD-2242-3AR', 'PWR-2411-DC-BLUE', Airflow.INTAKE),
   ]
   DESCRIPTION = psuDescHelper(
      sensors=[
         ('inlet', Position.OTHER, 60, 75, 85),
         ('secondary hotspot', Position.OTHER, 70, 120, 125),
         ('primary hotspot', Position.OTHER, 70, 110, 115),
      ],
      maxRpm=25500,
   )

class LiteOn2400HV(LiteonPsu):
   DRIVER = 'dps800'
   CAPACITY = 2400
   IDENTIFIERS = [
      PsuIdent('PS-2242-9A ', 'PWR-2422-HV-RED',  Airflow.EXHAUST),
   ]
   DESCRIPTION = psuDescHelper(
      sensors=[
         ('inlet', Position.OTHER, 60, 65, 70),
         ('secondary hotspot', Position.OTHER, 110, 120, 130),
         ('primary hotspot', Position.OTHER, 110, 115, 120),
      ],
      maxRpm=25500,
   )
