from __future__ import absolute_import

from multiprocessing import Process

from ...tests.testing import unittest, patch
from ...core.fabric import Fabric
from ...core.linecard import Linecard
from ...core.modular import Modular
from ...core.platform import loadPlatforms, getPlatforms
from ...core.supervisor import Supervisor
from .. import main

def fakesleep(_):
   pass

@patch('time.sleep', fakesleep)
class CliLegacyTest(unittest.TestCase):
   def _runMain(self, args, code=0):
      p = Process(target=main, args=(args,))
      p.start()
      p.join()
      self.assertEqual(p.exitcode, code,
                       msg='Command %s failed with code %s' % (args, p.exitcode))

   def testSysEeprom(self):
      self._runMain(['syseeprom'])

   def testPlatforms(self):
      self._runMain(['platforms'])

   def testHelpAll(self):
      self._runMain(['--help-all'])

   def _foreachPlatform(self, *args, **kwargs):
      code = kwargs.get('code', 0)
      ignoreSup = kwargs.get('ignoreSupervisor', False)
      ignoreTup = tuple([Modular, Fabric] + ([Supervisor] if ignoreSup else []))
      loadPlatforms()
      for platform in getPlatforms():
         if issubclass(platform, ignoreTup):
            continue
         if issubclass(platform, Linecard) and not platform.CPU_CLS:
            continue
         key = platform.SID[0] if platform.SID else platform.SKU[0]
         _args = ['-p', key, '-s'] + list(args)
         self._runMain(_args, code)

   def testSetup(self):
      self._foreachPlatform('setup')

   def testSetupBackground(self):
      self._foreachPlatform('setup', '--reset', '--background')

   def testResetToggle(self):
      self._foreachPlatform('reset', '--toggle')

   def testClean(self):
      self._foreachPlatform('clean')

   def testDump(self):
      self._foreachPlatform('dump', ignoreSupervisor=True)

   def testRebootCause(self):
      self._foreachPlatform('reboot-cause')

   def testDiag(self):
      self._foreachPlatform('platform', 'diag', '--noIo')

   def testDiagIo(self):
      # TODO: fix simulation mode
      #self._foreachPlatform('diag')
      pass

   def testWatchdogStatus(self):
      self._foreachPlatform('watchdog', '--status')

   def testWatchdogArm(self):
      self._foreachPlatform('watchdog', '--arm')

   def testWatchdogArmTimeout(self):
      self._foreachPlatform('watchdog', '--arm', '500')

   def testWatchdogStop(self):
      self._foreachPlatform('watchdog', '--stop')

if __name__ == '__main__':
   unittest.main()
