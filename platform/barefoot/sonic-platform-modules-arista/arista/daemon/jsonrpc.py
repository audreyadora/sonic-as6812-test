from ..core.daemon import registerDaemonFeature, OneShotFeature
from ..core.config import Config
from ..core.log import getLogger
from ..core.supervisor import Supervisor
from ..core.linecard import Linecard
from ..utils.rpc.api import RpcSupervisorApi, RpcLinecardApi
from ..utils.rpc.server import RpcServer

logging = getLogger(__name__)

@registerDaemonFeature()
class JsonRpcDaemonFeature(OneShotFeature):
   NAME = 'jsonrpc'

   def __init__(self):
      OneShotFeature.__init__(self)
      self.server = None

   def run(self):
      hosts = []
      api = None

      if isinstance(self.daemon.platform, Supervisor):
         logging.info('%s: setting up server on supervisor', self)
         hosts = [Config().api_rpc_host, Config().api_rpc_sup]
         api = RpcSupervisorApi(self.daemon.platform)
      elif isinstance(self.daemon.platform, Linecard):
         logging.info('%s: setting up server on linecard', self)
         hosts = [Config().api_rpc_lcx.format(self.daemon.platform.getSlotId())]
         api = RpcLinecardApi(self.daemon.platform)
      else:
         logging.info('%s: not supervisor or linecard, nothing to do', self)
         return

      port = Config().api_rpc_port
      self.server = RpcServer(hosts, port, api)
      self.daemon.loop.create_task(self.server.start())
