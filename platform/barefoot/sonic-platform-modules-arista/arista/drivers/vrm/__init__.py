
from ...core.driver.user.i2c import I2cDevDriver

class VrmI2cUserDriver(I2cDevDriver):

   IDENTIFY_SEQUENCE = []

   def _expect_read_word(self, reg, value):
      try:
         data = self.read_word_data(reg)
         return data == value
      except IOError:
         return False

   def _expect_fail_read_word(self, reg):
      try:
         self.read_word_data(reg)
         return False
      except IOError:
         return True

   def _identify(self, sequence):
      for reg, value in sequence:
         if value is None:
            if not self._expect_fail_read_word(reg):
               return False
         else:
            if not self._expect_read_word(reg, value):
               return False
      return True

   def identify(self):
      if isinstance(self.IDENTIFY_SEQUENCE, tuple):
         for seq in self.IDENTIFY_SEQUENCE:
            if self._identify(seq):
               return True
         return False
      return self._identify(self.IDENTIFY_SEQUENCE)

