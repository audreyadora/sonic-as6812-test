from __future__ import absolute_import, division, print_function

import os
import tempfile
from struct import pack, unpack

from ...tests.testing import unittest

from ..utils import FileResource, MmapResource, ResourceAccessor

class ResourceTestBase(object):
   class TestClass(unittest.TestCase):
      CLASS_TO_TEST = ResourceAccessor
      TEST_DATA = b'ABCDEFG1234567'

      def setUp(self):
         self.tempFile = tempfile.NamedTemporaryFile()
         self.tempFile.write(self.TEST_DATA)
         self.tempFile.flush()

      def testOpenFailure(self):
         res = self.CLASS_TO_TEST('NonExist')
         self.assertFalse(res.openResource())

      def testOkOpenAndCloseAlreadyClosed(self):
         res = self.CLASS_TO_TEST(self.tempFile.name)
         self.assertTrue(res.openResource())
         res.closeResource()
         res.closeResource()

      def _fmtChar(self, size):
         if size == 1:
            return 'B'
         if size == 2:
            return 'H'
         if size == 4:
            return 'L'

         assert False, "No support for FMT char size %d" % size
         return None

      def _testRead(self, addr, size, readMethod):
         readVal = readMethod(addr)
         readValPacked = pack('<%s' % self._fmtChar(size), readVal)
         refVal = self.TEST_DATA[addr : addr + size]
         self.assertEqual(readValPacked, refVal)

      def testRead8(self):
         with self.CLASS_TO_TEST(self.tempFile.name) as res:
            self._testRead(0, 1, res.read8)
            self._testRead(7, 1, res.read8)
            self._testRead(len(self.TEST_DATA) - 1, 1, res.read8)

      def testRead16(self):
         with self.CLASS_TO_TEST(self.tempFile.name) as res:
            self._testRead(0, 2, res.read16)
            self._testRead(7, 2, res.read16)
            self._testRead(len(self.TEST_DATA) - 2, 2, res.read16)

      def testRead32(self):
         with self.CLASS_TO_TEST(self.tempFile.name) as res:
            self._testRead(0, 4, res.read32)
            self._testRead(7, 4, res.read32)
            self._testRead(len(self.TEST_DATA) - 4, 4, res.read32)

      def _testWrite(self, addr, size, writeMethod):
         refVal = 0x10203040 >> (32 - size * 8)
         writeMethod(addr, refVal)

         self.tempFile.seek(addr, os.SEEK_SET)
         writtenData = self.tempFile.read(size)
         self.tempFile.flush()

         unpackedWrittenData = unpack('<%s' % self._fmtChar(size), writtenData)[0]

         self.assertEqual(unpackedWrittenData, refVal)

      def testWrite8(self):
         with self.CLASS_TO_TEST(self.tempFile.name) as res:
            self._testWrite(0, 1, res.write8)
            self._testWrite(7, 1, res.write8)
            self._testWrite(self.tempFile.tell() - 1, 1, res.write8)

      def testWrite16(self):
         with self.CLASS_TO_TEST(self.tempFile.name) as res:
            self._testWrite(0, 2, res.write16)
            self._testWrite(7, 2, res.write16)
            self._testWrite(self.tempFile.tell() - 2, 2, res.write16)

      def testWrite32(self):
         with self.CLASS_TO_TEST(self.tempFile.name) as res:
            self._testWrite(0, 4, res.write32)
            self._testWrite(7, 4, res.write32)
            self._testWrite(self.tempFile.tell() - 4, 4, res.write32)

class FileResourceTest(ResourceTestBase.TestClass):
   CLASS_TO_TEST = FileResource

   def testFileOffsetRead(self):
      with self.CLASS_TO_TEST(self.tempFile.name) as res:
         offset = res.file_.tell()
         res.read8(0x1)
         self.assertEqual(offset, res.file_.tell())
         res.read16(0x5)
         self.assertEqual(offset, res.file_.tell())
         res.read32(0x7)
         self.assertEqual(offset, res.file_.tell())

   def testFileOffsetWrite(self):
      with self.CLASS_TO_TEST(self.tempFile.name) as res:
         offset = res.file_.tell()
         res.write8(0x1, 0)
         self.assertEqual(offset, res.file_.tell())
         res.write16(0x5, 42)
         self.assertEqual(offset, res.file_.tell())
         res.write32(0x7, 125)
         self.assertEqual(offset, res.file_.tell())

class MmapResourceTest(ResourceTestBase.TestClass):
   CLASS_TO_TEST = MmapResource

if __name__ == '__main__':
   unittest.main()
