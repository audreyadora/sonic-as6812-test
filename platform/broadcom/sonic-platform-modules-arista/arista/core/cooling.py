import json
import os
from collections import deque

from ..libs.python import monotonicRaw

from .config import Config
from .log import getLogger
from .utils import inSimulation

logging = getLogger(__name__)

class Airflow(object):
   UNKNOWN = 'unknown'
   EXHAUST = 'exhaust'
   INTAKE = 'intake'

class HistoricalData(object):
   def __init__(self, name):
      self.name = name
      size = max(Config().cooling_data_points, 2)
      self.set = deque([(None, None)] * size, size)
      self.get = deque([(None, None)] * size, size)

   def getValue(self, now, value):
      self.get.append((now, value))
      return value

   def setValue(self, now, value):
      self.set.append((now, value))
      return value

   @property
   def lastSet(self):
      return self.set[-1][1]

   @property
   def lastGet(self):
      return self.get[-1][1]

   @property
   def data(self):
      return {
         'name': self.name,
         'get': list(self.get),
         'set': list(self.set),
      }

class CoolingObject(object):
   def __init__(self, name, inv=None):
      super().__init__()
      self.name = name
      self.data = HistoricalData(name)
      self.inv = inv
      self._initialized = False

   def __str__(self):
      return '%s(%s)' % (self.__class__.__name__, self.name)

   def dump(self):
      return self.data.data

class CoolingFanBase(CoolingObject):
   def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)

   @property
   def speed(self):
      return self.data.lastGet

   @speed.setter
   def speed(self, value):
      return self.data.getValue(monotonicRaw(), value)

   @property
   def current(self):
      return self.data.get[-1][1]

   @property
   def last(self):
      return self.data.get[-2][1]

   def setSpeed(self, value):
      assert self.inv is not None or self.api is not None
      if self.inv is not None:
         self.inv.setSpeed(value)
      else:
         self.api.set_speed(value)

   def set(self, now, value):
      try:
         self.setSpeed(value)
         return self.data.setValue(now, value)
      except Exception: # pylint: disable=broad-except
         logging.exception('%s failed to write speed', self)
         return None

class CoolingThermalBase(CoolingObject):
   def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)
      self.overheat = None
      self.critical = None

   @property
   def temperature(self):
      return self.data.lastGet

   @temperature.setter
   def temperature(self, value):
      return self.data.getValue(monotonicRaw(), value)

   @property
   def target(self):
      if self.inv is not None:
         return self.inv.getDesc().target
      return Config().cooling_target_factor * self.overheat

   def valid(self):
      return self.temperature is not None and \
             self.overheat is not None and \
             self.critical is not None

class ThermalInfo(object):
   def __init__(self, thermal, value, target, overheat):
      self.thermal = thermal
      self.value = value
      self.target = target
      self.overheat = overheat
      self.delta = value - target
      self.deltap = self.delta / (overheat - target)

   def __str__(self):
      kwargs = ', '.join('%s=%s' % (k, str(v)) for k, v in self.__dict__.items())
      return '%s(%s)' % (self.__class__.__name__, kwargs)

class ThermalInfos(object):
   def __init__(self, targetOffset):
      self.overheat = False
      self.targetOffset = targetOffset
      self.infos = []

   def process(self, thermal):
      if not thermal.valid():
         return

      maxTemp = min(thermal.overheat, thermal.critical)
      if not int(thermal.target) or not int(maxTemp):
         return

      value = thermal.temperature

      if value > maxTemp:
         logging.debug('%s: temp is above overheat threshold', thermal)
         self.overheat = True

      target = thermal.target + self.targetOffset
      info = ThermalInfo(thermal, value, target, maxTemp)
      logging.debug('%s', info)
      self.infos.append(info)

   def choose(self):
      if not self.infos:
         return None
      selected = self.infos[0]
      for info in self.infos[1:]:
         if info.deltap > selected.deltap:
            selected = info
      return selected

class CoolingZone(object):

   MAX_SPEED = 100

   def __init__(self, algo, name):
      self.algo = algo
      self.name = name
      self.maxDecrease = Config().cooling_max_decrease
      self.maxIncrease = Config().cooling_max_increase
      self.minSpeed = Config().cooling_min_speed
      self.targetOffset = Config().cooling_target_offset
      self.speed = HistoricalData('target')
      self.fans = None
      self.thermals = None
      self.initialized = False

   def __str__(self):
      return '%s(%s)' % (self.__class__.__name__, self.name)

   def load(self, fans=None, thermals=None):
      self.fans = fans or {}
      self.thermals = thermals or {}
      self.initialized = True

   def update(self):
      for f in self.fans.values():
         f.update()
      for t in self.thermals.values():
         t.update()

   @property
   def lastSpeed(self):
      return self.speed.lastSet

   def computeFanSpeed(self, lastSpeed, infos):
      if infos.overheat:
         # Run the fans at 100% if one sensor is in overheat state
         return self.MAX_SPEED

      # Select the most critical sensor in the system
      info = infos.choose()
      if info is None:
         # No sensor found, run at 100%
         return self.MAX_SPEED

      logging.debug('%s: using %s to set fan speed', self, info.thermal)

      # Skip any fan speed change if the temperature to target delta is below
      # 5% of the target to overheat range.
      if abs(info.deltap * 100.) < 5.:
         return lastSpeed

      if info.delta < 0:
         speedDelta = max(self.maxDecrease * info.deltap, -self.maxDecrease)
      else:
         speedDelta = min(self.maxIncrease * info.deltap, self.maxIncrease)

      # adjust speed delta based on elapsed time
      speedDelta = self.scaleOnElapsed(speedDelta)

      # Enforce fan speed limits
      speed = max(lastSpeed + speedDelta, self.minSpeed)
      speed = min(speed, self.MAX_SPEED)

      return speed

   def scaleOnElapsed(self, value):
      factor = min(self.algo.elapsed / self.algo.INTERVAL, 1.0)
      return value * factor

   def readLastSpeed(self):
      lastSpeed = self.lastSpeed

      # Read the current fan speed to have it stored in the data
      for fan in self.fans.values():
         currentSpeed = fan.speed
         if lastSpeed is None: # useful when no speed has been set by the algo
            logging.debug('%s: detected last speed %d', self, currentSpeed)
            lastSpeed = currentSpeed

      if lastSpeed is None:
         logging.debug('%s: could not find last speed, assuming max', self)
         lastSpeed = self.MAX_SPEED

      return lastSpeed

   def run(self, fans=None, thermals=None, update=False):
      if not self.initialized:
         self.load(fans=fans, thermals=thermals)
      if update:
         self.update()

      lastSpeed = self.readLastSpeed()

      infos = ThermalInfos(self.targetOffset)
      for thermal in self.thermals.values():
         infos.process(thermal)

      desiredSpeed = self.computeFanSpeed(lastSpeed, infos)

      logging.debug('%s: fan speed selected is %.3f', self, desiredSpeed)
      self.speed.setValue(self.algo.now, desiredSpeed)

      # Set new fan speed
      for fan in self.fans.values():
         fan.set(self.algo.now, desiredSpeed)

   def export(self, path):
      data = {
         'name': self.name,
         'fans': [ f.dump() for f in self.fans.values() ],
         'thermals': [ t.dump() for t in self.thermals.values() ],
      }
      path = os.path.join(path, '%s.cooling.json' % self.name)
      with open(path, 'w', encoding='utf8') as f:
         json.dump(data, f)

class CoolingAlgorithm(object):

   INTERVAL = 60.

   def __init__(self, platform):
      self.platform = platform
      self.previous = None
      self.now = None
      self.elapsed = None
      self.zones = []
      self.load()

   def __str__(self):
      return '%s()' % self.__class__.__name__

   def load(self):
      # NOTE: for now only one zone
      self.zones.append(CoolingZone(self, 'System'))

   def export(self, path):
      if inSimulation():
         return
      for zone in self.zones:
         zone.export(path)

   def run(self, elapsed=None, fans=None, thermals=None, update=False):
      self.previous = self.now
      self.now = monotonicRaw()
      if self.previous is None:
         self.previous = self.now - self.INTERVAL
      self.elapsed = elapsed or self.now - self.previous

      logging.debug('%s: running algorithm (elapsed %.4fs)', self, self.elapsed)
      for zone in self.zones:
         zone.run(fans=fans, thermals=thermals, update=update)
      logging.debug('%s: algorithm took %.4fs to run', self,
                    monotonicRaw() - self.now)

      if Config().cooling_export_path:
         self.export(Config().cooling_export_path)
