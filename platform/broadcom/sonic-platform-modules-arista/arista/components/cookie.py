
from datetime import datetime
import os
import json
import re

from ..core.cause import ReloadCauseEntry, ReloadCauseProviderHelper
from ..core.component.component import Component
from ..core.config import flashPath
from ..core.log import getLogger
from ..descs.cause import ReloadCausePriority, ReloadCauseScore, ReloadCauseDesc
from ..drivers.cookie import SonicReloadCauseCookieDriver
from ..libs.date import datetimeToStr, strToDatetime

logging = getLogger(__name__)

REBOOT_CMD_MSG_RE = re.compile(
   r"User issued '(?P<command>.+?)' command \[.*Time: (?P<time>.*)\]")

class CookiePriority(ReloadCausePriority):
   pass

class CookieReloadCauseEntry(ReloadCauseEntry):
   pass

class CookieReloadCauseProvider(ReloadCauseProviderHelper):
   def __init__(self, cookies, slotId):
      assert slotId is not None and isinstance(slotId, int), \
         "invalid slotId"
      sourceName = f'cookie-slot{slotId}' if slotId else 'cookie-platform'
      super().__init__(sourceName)
      self.cookies = cookies
      self.slotId = slotId
      self.callbacks = []

   def process(self):
      self.cookies.loadCookieFile()
      self.causes = self.cookies.getReloadCauses()
      self.cookies.reset()

class SonicReloadCauseProvider(ReloadCauseProviderHelper):
   def __init__(self, cookie):
      super().__init__(str(cookie))
      self.cookie = cookie

   def process(self):
      self.causes = self.cookie.getReloadCauses()

class SonicReloadCauseCookieComponent(Component):
   DRIVER = SonicReloadCauseCookieDriver

   def __init__(self, *args, **kwargs):
      super().__init__(*args, **kwargs)
      self.inventory.addReloadCauseProvider(SonicReloadCauseProvider(self))

   def _fixTime(self, timestamp):
      # FIXME: The date format is locale-dependent
      try:
         dt = strToDatetime(timestamp, fmt='%a %d %b %Y %I:%M:%S %p %Z')
      except ValueError:
         try:
            dt = strToDatetime(timestamp, fmt='%a %b %d %H:%M:%S %Z %Y')
         except ValueError:
            return 'unknown'
      return datetimeToStr(dt)

   def getReloadCauses(self):
      causeStr = self.driver.getSoftwareCause()
      logging.debug('Got reboot cause from cookie file: %s', causeStr)
      if not causeStr:
         return []

      m = REBOOT_CMD_MSG_RE.match(causeStr)
      if m:
         logging.debug('Reboot cause is user reboot')
         return [
            CookieReloadCauseEntry(
               'reboot', self._fixTime(m.group('time')),
               rcDesc="User issued '{}' command".format(m.group('command')),
               score=ReloadCauseScore.LOGGED |
                     ReloadCauseScore.EVENT |
                     ReloadCauseScore.DETAILED |
                     ReloadCauseScore.getPriority(CookiePriority.HIGH))
         ]
      return []

class CookieComponentBase(Component):
   VERSION = 1
   DEFAULT_CAUSEDATA = {
      'version': VERSION,
      'platform': {},
      'slots': {},
   }

   def __init__(self, slotId=None, **kwargs):
      super().__init__(**kwargs)
      self.slotId = slotId
      self.inventory.addReloadCauseProvider(CookieReloadCauseProvider(self, slotId))
      self.callbacks = []
      self.causeData = {}

   def register(self, cause, testCallback):
      self.callbacks.append((cause, testCallback))

   def poll(self):
      for cause, testCb in self.callbacks:
         if cause not in self.causeData and testCb():
            logging.debug('callback for cause "%s" succeeded on slot %d',
                          cause, self.slotId)
            desc = ReloadCauseDesc(0x0, cause, priority=ReloadCausePriority.HIGH)
            time = datetimeToStr(datetime.now())
            self.causeData[cause] = ReloadCauseEntry(
               cause=desc.typ,
               rcTime=time,
               rcDesc=desc.description,
               score=ReloadCauseScore.LOGGED | ReloadCauseScore.DETAILED |
                     ReloadCauseScore.getPriority(desc.priority))

   def reset(self):
      self.causeData = {}

   def loadCookieFile(self):
      raise NotImplementedError

   def causesFromDict(self, newCauses):
      for cause, entry in newCauses.items():
         self.causeData[cause] = ReloadCauseEntry.fromDict(entry)

   def causesToDict(self):
      return {c : e.toDict() for c, e in self.causeData.items()}

   def getReloadCauses(self):
      return list(self.causeData.values())

class SlotCookieComponent(CookieComponentBase):
   def __init__(self, slotId=None, platformCookies=None, **kwargs):
      assert slotId is not None
      assert platformCookies is not None
      super().__init__(slotId=slotId, **kwargs)
      self.platformCookies = platformCookies

   def reset(self):
      super().reset()
      self.platformCookies.storeCauses()

   def loadCookieFile(self):
      self.platformCookies.loadCookieFile()

class PlatformCookieComponent(CookieComponentBase):
   def __init__(self, path=None, **kwargs):
      super().__init__(slotId=0, **kwargs)
      self.path = path or flashPath('reboot-cause', 'platform', 'cookies.json')
      self.slots = {}
      self.lastStoredData = {}
      self.platformIoErrorReported = False
      self.slotIoErrorReported = {}

   def loadCookieFile(self):
      if not os.path.exists(self.path):
         return None

      with open(self.path, 'r', encoding='utf-8') as f:
         try:
            return json.load(f)
         except (ValueError, KeyError):
            logging.exception("Failed to parse reload cause cookie data from %s",
                              self.path)
      return None

   def fromDict(self, data):
      if data['version'] != self.VERSION:
         raise ValueError(f'Expected reload cause version to be {self.VERSION}')
      self.causesFromDict(data['platform'])
      for slotIdStr, sources in data['slots'].items():
         slotId = int(slotIdStr)
         if slotId not in self.slots:
            raise ValueError(f'Unexpected slotId {slotId} in cookie data')
         # JSON keys are always stored as strings
         self.slots[slotId].causesFromDict(sources)

   def toDict(self):
      data = {}
      data['version'] = self.VERSION
      data['platform'] = self.causesToDict()
      data['slots'] = {}
      for slotId, slotCookies in self.slots.items():
         slotData = slotCookies.causesToDict()
         if slotData:
            data['slots'][slotId] = slotData
      return data

   def addLinecard(self, card):
      slot = card.slot
      slotCookies = card.newComponent(SlotCookieComponent, slotId=slot.slotId,
                                      platformCookies=self)
      self.slots[slot.slotId] = slotCookies
      card.cookies = slotCookies

   def poll(self):
      try:
         super().poll()
         self.platformIoErrorReported = False
      except IOError:
         if not self.platformIoErrorReported:
            logging.info('IO error reported polling platform reboot causes',
                         exc_info=True)
            self.platformIoErrorReported = True
      for slotId, slotCookies in self.slots.items():
         try:
            slotCookies.poll()
            if self.slotIoErrorReported.get(slotId, False):
               logging.info('cookie: Connectivity restored to linecard %d', slotId)
               self.slotIoErrorReported[slotId] = False
         except IOError:
            if not self.slotIoErrorReported.get(slotId, False):
               logging.info('cookie: Connectivity lost to linecard %d', slotId,
                            exc_info=slotId not in self.slotIoErrorReported)
               self.slotIoErrorReported[slotId] = True

   def storeCauses(self):
      data = self.toDict()
      if data != self.lastStoredData:
         with open(self.path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=3, separators=(',', ': '), sort_keys=True)
         self.lastStoredData = data
