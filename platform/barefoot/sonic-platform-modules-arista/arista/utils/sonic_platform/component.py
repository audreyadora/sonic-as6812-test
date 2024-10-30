
try:
   from sonic_platform_base.component_base import ComponentBase
except ImportError as e:
   raise ImportError("%s - required module not found" % e) from e

_fwApi = None
_fwApiLoaded = False

class Component(ComponentBase):
   def __init__(self, parent, programmable):
      self.parent = parent
      self.programmable = programmable
      self.api = self.fwapi.get_component(self) if self.fwapi else None

   @property
   def fwapi(self):
      global _fwApi, _fwApiLoaded # pylint: disable=global-statement
      if not _fwApiLoaded:
         try:
            # pylint: disable=import-outside-toplevel
            from arista_fwutil.api import Api
            _fwApi = Api()
         except ImportError:
            pass
         _fwApiLoaded = True
      return _fwApi

   def get_name(self):
      return str(self.programmable.getComponent())

   def get_presence(self):
      return True

   def get_model(self):
      return self.programmable.getComponent().__class__.__name__

   def get_serial(self):
      return 'N/A'

   def get_status(self):
      return True

   def get_description(self):
      return self.programmable.getDescription()

   def get_position_in_parent(self):
      return -1

   def is_replaceable(self):
      return False

   def get_firmware_version(self):
      if self.api is not None:
         return self.api.get_firmware_version()
      return self.programmable.getVersion()

   def get_available_firmware_version(self, image_path):
      if self.api is not None:
         return self.api.get_available_firmware_version(image_path)
      return self.get_firmware_version()

   def get_firmware_update_notification(self, image_path):
      if self.api is not None:
         return self.api.get_firmware_update_notification(image_path)
      return "None"

   def install_firmware(self, image_path):
      if self.api is not None:
         return self.api.install_firmware(image_path)
      return True

   def update_firmware(self, image_path):
      if self.api is not None:
         return self.api.update_firmware(image_path)
      return True

   def auto_update_firmware(self, image_path, boot_type):
      if self.api is not None:
         return self.api.auto_update_firmware(image_path, boot_type)
      return 1
