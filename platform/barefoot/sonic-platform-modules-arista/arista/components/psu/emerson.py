from ...core.cooling import Airflow
from ...core.psu import PsuModel, PsuIdent

from . import PmbusPsu
from .helper import psuDescHelper, Position

class EmersonPsu(PsuModel):
   MANUFACTURER = 'emerson'
   PMBUS_ADDR = 0x58

   PMBUS_CLS = PmbusPsu

class DS750PED(EmersonPsu):
   CAPACITY = 750
   DESCRIPTION = psuDescHelper(
      sensors=[
         ('hotspot', Position.OTHER, 85, 100, 105),
         ('ambiant', Position.OTHER, 55, 70, 75),
      ],
   )
   IDENTIFIERS = [
      PsuIdent('DS750PED-3',     'PWR-745AC-F', Airflow.EXHAUST),
      PsuIdent('DS750PED-3-001', 'PWR-745AC-R', Airflow.INTAKE),
      PsuIdent('DS750PED-3-402', 'PWR-745AC-R', Airflow.INTAKE),
      PsuIdent('DS750PED-3-403', 'PWR-745AC-F', Airflow.EXHAUST),
   ]
