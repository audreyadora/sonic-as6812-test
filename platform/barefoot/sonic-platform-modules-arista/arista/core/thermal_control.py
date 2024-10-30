from __future__ import absolute_import, division, print_function

MIN_FAN_SPEED = 30
MAX_FAN_SPEED = 100

def sensorsToFanSpeed(sensors):
   targetFanSpeed = MIN_FAN_SPEED
   for sensor in sensors:
      if not sensor.get_presence():
         continue
      desc = sensor.get_inventory_object().getDesc()
      maxTemp = min(desc.overheat, desc.critical)
      if not int(desc.target) or not int(maxTemp):
         continue
      halfwayTemp = (desc.target + maxTemp) / 2
      temp = sensor.get_temperature()
      if temp < halfwayTemp:
         continue
      elif temp >= maxTemp:
         targetFanSpeed = MAX_FAN_SPEED
         continue
      newFanSpeed = (temp - halfwayTemp) / (maxTemp - halfwayTemp) * \
                    (MAX_FAN_SPEED - MIN_FAN_SPEED) + \
                    MIN_FAN_SPEED
      targetFanSpeed = max(targetFanSpeed, newFanSpeed)
   return targetFanSpeed
