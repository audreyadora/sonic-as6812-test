
from ...descs.fan import FanDesc, FanPosition
from ...descs.psu import PsuDesc
from ...descs.rail import RailDesc, RailDirection
from ...descs.sensor import Position, SensorDesc

def psuDescHelper(hasFans=True, maxRpm=None, minRpm=0,
                  inputRailId=1, inputMaxVoltage=None, inputMinVoltage=None,
                  outputRailId=1, outputMaxVoltage=None, outputMinVoltage=None,
                  sensors=None):
   fans = [
      FanDesc(
         fanId=1,
         name='psu%(psuId)d/%(fanId)d',
         position=FanPosition.OUTLET,
         maxRpm=maxRpm,
         minRpm=minRpm
      )
   ] if hasFans else []

   rails = []
   if inputRailId is not None:
      rails.append(RailDesc(
         railId=inputRailId,
         direction=RailDirection.INPUT,
         maxVoltage=inputMaxVoltage,
         minVoltage=inputMinVoltage,
      ))
   if outputRailId is not None:
      rails.append(RailDesc(
         railId=outputRailId,
         direction=RailDirection.OUTPUT,
         maxVoltage=outputMaxVoltage,
         minVoltage=outputMinVoltage,
      ))

   sensors = sensors or []
   sensors=[
      SensorDesc(
         diode=i,
         name='Power supply %%(psuId)d %s sensor' % name,
         position=position,
         target=target,
         overheat=overheat,
         critical=critical,
      )
      for i, (name, position, target, overheat, critical) in enumerate(sensors)
   ]

   return PsuDesc(fans=fans, rails=rails, sensors=sensors)
