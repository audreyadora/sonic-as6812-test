
import subprocess

from .log import getLogger
from .utils import inSimulation

logging = getLogger(__name__)

class Quirk(object):

   DELAYED = False

   def run(self, component):
      raise NotImplementedError

class QuirkCmd(Quirk):
   def __init__(self, cmd, description):
      self.description = description
      self.cmd = cmd

   def __str__(self):
      return self.description

   def run(self, component):
      if not inSimulation():
         subprocess.check_output(self.cmd)

class PciConfigQuirk(QuirkCmd): # TODO: reparent when using PciTopology
   def __init__(self, addr, expr, description):
      super().__init__(['setpci', '-s', str(addr), expr], description)
      self.addr = addr
      self.expr = expr
