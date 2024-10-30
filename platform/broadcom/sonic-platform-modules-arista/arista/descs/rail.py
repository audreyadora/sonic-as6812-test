
from ..core.desc import HwDesc

class RailDirection(object):
   INPUT = 'input'
   OUTPUT = 'output'

class RailDesc(HwDesc):

   OID_FIELD = 'railId'

   def __init__(self, railId, name='%(direction)s%(railId)s', direction=None,
                current=None, power=None, voltage=None, **kwargs):
      super(RailDesc, self).__init__(**kwargs)
      self.railId = railId
      self.fmt = name
      self.direction = direction
      self.name = None
      self.current = current
      self.power = power
      self.voltage = voltage

   def renderName(self, **kwargs):
      values = kwargs.copy()
      values.update(self.__dict__)
      self.name = self.fmt % values

class VoltageDesc(HwDesc):

   OID_FIELD = 'voltId'

   def __init__(self, voltId, name=None, direction=None, **kwargs):
      super(VoltageDesc, self).__init__(**kwargs)
      self.voltId = voltId
      self.name = name
      self.direction = direction

class CurrentDesc(HwDesc):

   OID_FIELD = 'currId'

   def __init__(self, currId, name=None, direction=None, **kwargs):
      super(CurrentDesc, self).__init__(**kwargs)
      self.currId = currId
      self.name = name
      self.direction = direction

class PowerDesc(HwDesc):

   OID_FIELD = 'powerId'

   def __init__(self, powerId, name=None, direction=None, **kwargs):
      super(PowerDesc, self).__init__(**kwargs)
      self.powerId = powerId
      self.name = name
      self.direction = direction
