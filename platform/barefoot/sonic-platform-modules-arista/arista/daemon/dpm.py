
from ..core.daemon import registerDaemonFeature, PollDaemonFeature
from ..core.log import getLogger

logging = getLogger(__name__)

@registerDaemonFeature()
class DpmMonitorFeature(PollDaemonFeature):

   NAME = 'dpm'
   INTERVAL = 10 * 60

   def init(self):
      PollDaemonFeature.init(self)
      self.providers = []
      for rcp in self.daemon.platform.getInventory().getReloadCauseProviders():
         logging.info('%s: %s marked for periodic clock sync', self, rcp)
         self.providers.append(rcp)

   def callback(self, elapsed):
      for rcp in self.providers:
         logging.debug('%s: updating %s rtc', self, rcp)
         rcp.setRealTimeClock()
