
from ...components.dpm.pmbus import PmbusDpm
from ...core.diag import DiagContext

from . import Renderer, List, Row

class ShowPower(Renderer):

   NAME = 'power'

   def getData(self, show):
      ctx = DiagContext()
      data = {
         'slots': [],
         'dpms': [],
      }
      for platform in show.platforms:
         for slot in platform.getInventory().getPsuSlots():
            data['slots'].append(slot.__diag__(ctx))
         # TODO: for dpm in inventory.getPowerControllers():
         for component in platform.iterComponents(recursive=True, filters=None):
            if isinstance(component, PmbusDpm):
               data['dpms'].append(component.__diag__(ctx))
      return data

   def renderText(self, show):
      data = self.data(show)

      List("Power Supplies:", header=("PSU%d", 'slotId'), tree=[
         Row('Present: %s', 'present'),
         Row('Status: %s (%s)', 'status', 'led.color'),
         Row('Model: %s', 'psu.model'),
         Row('Serial: %s', 'psu.serial'),
         Row('MfrModel: %s (%s)', 'psu.mfr.model', 'psu.mfr.revision'),
         Row('MfrFab: %s (%s)', 'psu.mfr.location', 'psu.mfr.date'),
         Row('Capacity: %s Watts', 'psu.capacity'),
         List('Fans:', attr='psu.fans', header=('%s', 'name'), tree=[
            Row('Speed: %s RPM (%s)', 'rpm', 'status'),
         ]),
         List('Thermal:', attr='psu.temps', header=('%s', 'name'), tree=[
            Row('Temperature: %s Celcius', 'value'),
         ]),
         List('Rails:', attr='psu.rails', header=('%s', 'name'), tree=[
            Row('Voltage: %s Volts', 'voltage'),
            Row('Current: %s Amps', 'current'),
            Row('Power: %s Watts', 'power'),
         ]),
      ]).render(data['slots'], newline=True)

      List(title="Power Controllers:", header=('%s', 'name'), tree=[
         Row('Version: %s', 'version'),
         # TODO: add fields
      ]).render(data['dpms'])
