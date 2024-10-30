from ..core.desc import HwDesc

class Xcvr(HwDesc):
   LANES = None
   SPEED = None

   def __init__(self, index, speed=None, lanes=None, leds=1, **kwargs):
      super(Xcvr, self).__init__(**kwargs)
      self.index = index
      self.leds = leds
      self.lanes = lanes or self.LANES
      self.speed = speed or self.SPEED

   def __str__(self):
      return f'{self.__class__.__name__}(index={self.index})'

class Rj45(Xcvr):
   LANES = 1
   SPEED = 1000

class Sfp(Xcvr):
   LANES = 1
   SPEED = 10000

class Sfp28(Sfp):
   SPEED = 25000

class Sfp56(Sfp28):
   SPEED = 50000

class Qsfp(Xcvr):
   LANES = 4
   SPEED = 10000

class QsfpPlus(Qsfp):
   pass

class Qsfp28(QsfpPlus):
   SPEED = 25000

class Qsfp56(Qsfp28):
   SPEED = 50000

class QsfpDD(Qsfp56):
   LANES = 8

class Osfp(Xcvr):
   LANES = 8
   SPEED = 50000
