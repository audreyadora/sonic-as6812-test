"""
This file provides helper for sonic environment

Currently all arista switches have their eeprom at the same address and use
the same data format. Since it is not an open standard and all our platforms
need this having everything at the same place is easier.

The eeprom plugin end up being just the following

   import arista.utils.sonic_eeprom
   board = arista.utils.sonic_eeprom.getTlvInfoDecoder()

We should be able to remove "getTlvInfoDecoder" after we change it on
sonic-buildimage, and do:

   from arista.utils.sonic_eeprom import board
"""

from ..core.platform import fmted_prefdl_path, readPrefdl

try:
   from sonic_platform_base.sonic_eeprom import eeprom_base
except ImportError as error:
   raise ImportError("%s - required module not found" % error)

class board(eeprom_base.EepromDecoder):
   def __init__(self, path, format, start, status, readonly=True):
      # pylint: disable=redefined-builtin
      self._prefdl_cache = {}
      self.prefdl_path = fmted_prefdl_path
      super(board, self).__init__(self.prefdl_path, format, start, status, True)

   def read_eeprom(self):
      return readPrefdl()

   def set_eeprom(self, e, cmd_args):
      raise NotImplementedError

   def decode_eeprom(self, e):
      return e.show()

   def is_checksum_valid(self, e):
      return (e.isCrcValid(), e.getCrc())

   def serial_number_str(self, e):
      return e.getField('SerialNumber')

   def base_mac_addr(self, e):
      return e.getField('MAC')

   def get_eeprom_dict(self, e):
      return {'Data': e.toDict()}

   def modelstr(self, e):
      return e.getField('SKU')

def getTlvInfoDecoder():
   return board
