from ...components.pali import Pali2

from ...core.fixed import FixedChassis

class MaunaKea2(FixedChassis):

   FAN_COUNT = 4

   @classmethod
   def addFanboard(cls, parent, bus):
      return Pali2(parent, bus)
