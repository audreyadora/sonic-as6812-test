from enum import IntEnum

class JsonRpcError(IntEnum):
   """Error codes defined by the JSON-RPC specification."""
   PARSE_ERROR = -32700
   INVALID_REQUEST = -32600
   METHOD_NOT_FOUND = -32601
   INVALID_PARAMS = -32602
   INTERNAL_ERROR = -32603

JSONRPC_VERSION = '2.0'
