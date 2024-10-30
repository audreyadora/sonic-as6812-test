
try:
   from sonic_platform_base.fan_drawer_base import FanDrawerBase
   from .fan import Fan
except ImportError as e:
   raise ImportError("%s - required module not found" % e)

class FanDrawer(FanDrawerBase):
   def __init__(self, parent, slot):
      FanDrawerBase.__init__(self)
      self._parent = parent
      self._fan_list = [Fan(self, fan) for fan in slot.getFans()]
      self._slot = slot
      self._hotswappable = True

   def get_name(self):
      return self._slot.getName()

   def get_model(self):
      try:
         return self._slot.getModel()
      except Exception: # pylint: disable=broad-except
         return 'N/A'

   def get_presence(self):
      return self._slot.getPresence()

   def get_serial(self):
      return 'N/A'

   def get_revision(self):
      return 'N/A'

   def get_status(self):
      return self._slot.getPresence() and not self._slot.getFault()

   def get_status_led(self, color=None):
      led = self._slot.getLed()
      if led is None:
         return None
      return led.getColor()

   def set_status_led(self, color):
      led = self._slot.getLed()
      if led is None:
         return True
      try:
         led.setColor(color)
         return True
      except (IOError, OSError, ValueError):
         return False

   def get_maximum_consumed_power(self):
      return float(self._slot.getMaxPowerDraw())

   def get_position_in_parent(self):
      return self._slot.getId()

   def is_replaceable(self):
      return self._hotswappable

   def get_interrupt_file(self):
      return None

class FixedFanDrawer(FanDrawerBase):
   def __init__(self, parent, fan):
      FanDrawerBase.__init__(self)
      self._parent = parent
      self._inv = fan
      self._fan = Fan(self, fan)
      self._fan_list = [self._fan]
      self._hotswappable = False

   def get_name(self):
      return 'fixed%s' % self._inv.getId()

   def get_model(self):
      return self._fan.get_model()

   def get_presence(self):
      return True

   def get_serial(self):
      return self._fan.get_serial()

   def get_status(self):
      return self._fan.get_status()

   def get_status_led(self, color=None):
      led = self._inv.getLed()
      if led is None:
         return None
      return led.getColor()

   def set_status_led(self, color):
      led = self._inv.getLed()
      if led is None:
         return None
      try:
         led.setColor(color)
         return True
      except (IOError, OSError, ValueError):
         return False

   def get_maximum_consumed_power(self):
      # TODO: report fan consumption information
      return 0.

   def get_position_in_parent(self):
      return self._inv.getId()

   def is_replaceable(self):
      return self._hotswappable

   def get_interrupt_file(self):
      return None
