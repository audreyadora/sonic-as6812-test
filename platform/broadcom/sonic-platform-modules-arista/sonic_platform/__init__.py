# redirect sonic_platform implementation to arista.utils.sonic_platform
# this is essentially a python package symlink
__path__ = [
   __path__[0].replace('sonic_platform', 'arista/utils/sonic_platform')
]

# import all modules since some tools expects it
from . import (
   chassis,
   component,
   fan,
   fan_drawer,
   module,
   pcie,
   platform,
   psu,
   sfp,
   thermal,
   thermal_manager,
   watchdog,
)
