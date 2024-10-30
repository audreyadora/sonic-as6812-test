
from ..core.log import getLogger

from ..core.driver.user.i2c import I2cDevDriver

logging = getLogger(__name__)

class Ds125BrDevDriver(I2cDevDriver):

   def __init__(self, amplitude=None, channels=8, **kwargs):
      super(Ds125BrDevDriver, self).__init__(**kwargs)
      self.channels = channels
      self.amplitude = amplitude
      self.config = self.qsfpPortConfig(amplitude) if amplitude else \
                    self.qsfpPortGroupConfig()

   def qsfpPortConfig(self, amplitude):
      disableCrc = 0x18
      squelchMode = 0x40
      outputAmplitude = amplitude
      assert len(outputAmplitude) == self.channels
      txDeEmphasis = [0x00] * self.channels
      rxEqualization = [0x00] * self.channels
      inputTermination = [0x0c] * self.channels
      squelch = [0x02] * self.channels
      return [disableCrc, squelchMode, outputAmplitude, txDeEmphasis,
              rxEqualization, inputTermination, squelch]

   def qsfpPortGroupConfig(self):
      portConfig = self.qsfpPortConfig([None, 0xac, None, 0xac,
                                        0xab, 0xab, 0xab, 0xac])
      txDeEmphasis = portConfig[3]
      txDeEmphasis[0] = None
      txDeEmphasis[2] = None
      portConfig[3] = txDeEmphasis
      return portConfig

   def setupPort(self, config):
      disableCrc, squelchMode, outputAmplitude, txDeEmphasis, \
                  rxEqualization, inputTermination, squelch = config

      self.write_byte_data(0x06, disableCrc)
      self.write_byte_data(0x28, squelchMode)

      baseAddr = 0x0d
      for channel in range(0, self.channels):
         offset = channel * 7
         if (baseAddr + offset) > 0x27:
            offset += 1
         regs = [
            (baseAddr + offset + 0, squelch[channel]),
            (baseAddr + offset + 1, inputTermination[channel]),
            (baseAddr + offset + 2, rxEqualization[channel]),
            (baseAddr + offset + 3, outputAmplitude[channel]),
            (baseAddr + offset + 4, txDeEmphasis[channel]),
         ]
         for reg, data in regs:
            if data is not None:
               logging.debug('i2c-write %#02x %#02x %#02x', self.addr.address, reg,
                             data)
               self.write_byte_data(reg, data)

   def setup(self):
      logging.debug('%s: setting up repeater', self)
      self.setupPort(self.config)
