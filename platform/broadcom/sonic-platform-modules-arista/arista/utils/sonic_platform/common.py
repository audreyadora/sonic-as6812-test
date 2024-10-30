from enum import Enum

try:
   from arista.core.config import Config
   from arista.utils.rpc.client import RpcClient
except ImportError as e:
   raise ImportError("%s - Required module not found" % e)

_globalRpcClient = None

class RpcClientSource(Enum):
   FROM_SUPERVISOR = 1
   FROM_LINECARD = 2

def getGlobalRpcClient(source):
   global _globalRpcClient
   if _globalRpcClient is None:
      host = ( Config().api_rpc_sup if source is RpcClientSource.FROM_LINECARD
               else Config().api_rpc_host )
      _globalRpcClient = RpcClient(host, Config().api_rpc_port)
   return _globalRpcClient
