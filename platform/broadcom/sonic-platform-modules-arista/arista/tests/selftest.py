
from ..core.log import getLogger

import unittest

logger = getLogger( __name__ )

def allTests():
   import setuptools
   suite = unittest.TestSuite()
   for path in setuptools.findall( 'arista' ):
      if '/tests/' in path and '__init__.py' not in path and path.endswith( '.py' ):
         module = path[ : -3 ].replace( '/', '.' )
         logger.info( 'test-suite: adding %s', module )
         suite.addTests( unittest.defaultTestLoader.loadTestsFromName( module ) )
   return suite
