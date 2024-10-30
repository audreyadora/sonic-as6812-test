try:
   import asyncio
except ImportError:
   # This file shouldn't be packaged for python2 but just in case
   print('This feature only works in python3')
   raise

from .config import Config
from .linecard import LCpuCtx
from .log import getLogger
from .utils import clog
from ..utils.rpc.client import RpcClient

logging = getLogger(__name__)

class LinecardRebootManager(object):
   def __init__(self, chassis, linecards=None):
      self.loop = asyncio.get_event_loop()
      self.chassis = chassis

      if linecards is None:
         self.linecards = [lc for lc in self.chassis.iterLinecards()
                           if lc.getPresence() and lc.poweredOn()]
      else:
         self.linecards = linecards

   def doReboot(self, linecard):
      if linecard.getPresence() and linecard.hasCpuModule():
         client = RpcClient(Config().api_rpc_lcx.format(linecard.getSlotId()),
                            Config().api_rpc_port)
         client.gracefulShutdown()

   async def _linecardEarlyBoot(self, linecard):
      while True:
         if linecard.getLastPostCode() not in [0x00, 0x9e]:
            return True
         await asyncio.sleep(0.1)

   async def _async_powerOffLinecard(self, linecard):
      if linecard.getPresence() and linecard.hasCpuModule():
         try:
            logging.info('Start graceful reboot on linecard %s...', linecard)
            self.doReboot(linecard)
         except: # pylint: disable=bare-except
            logging.exception('Graceful reboot on linecard %s failed', linecard)
         else:
            try:
               await asyncio.wait_for(self._linecardEarlyBoot(linecard), timeout=60)
               logging.info('Graceful reboot on linecard %s complete', linecard)
            except asyncio.TimeoutError:
               logging.warning('Linecard %s shutdown timed out, '
                               'forcing power off...', linecard)

      try:
         logging.debug('Power off linecard %s...', linecard)
         if linecard.slot.getPresence() and linecard.poweredOn():
            linecard.powerOnIs(False)
            logging.info('Power off linecard %s success', linecard)
         else:
            logging.info('Power off linecard %s skipped', linecard)
      except Exception as e:  # pylint: disable=broad-except
         logging.exception('Power off linecard %s failed', linecard)
         clog('Failed to power off linecard %s: %s', linecard, e)

   async def _async_powerOffLinecards(self):
      tasks = []
      for linecard in self.linecards:
         tasks.append(self.loop.create_task(
            self._async_powerOffLinecard(linecard)))
      await asyncio.gather(*tasks)

   def powerOffLinecards(self):
      return self.loop.run_until_complete(self._async_powerOffLinecards())

   def rebootLinecards(self, mode='soft'):
      if mode == 'hard':
         self.powerOffLinecards()
         lcpuCtx = LCpuCtx()
         for linecard in self.linecards:
            try:
               logging.debug('Power on linecard %s...', linecard)
               linecard.powerOnIs(True, lcpuCtx)
            except: # pylint: disable=bare-except
               logging.exception('Start linecard %s failed', linecard)
      else:
         for linecard in self.linecards:
            try:
               logging.info('Reboot linecard %s...', linecard)
               self.doReboot(linecard)
               logging.info('Reboot linecard %s success', linecard)
            except: # pylint: disable=bare-except
               logging.exception('Reboot linecard %s failed', linecard)
