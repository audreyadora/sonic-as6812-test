from errno import EAGAIN
import json
import os
import select

from ....tests.testing import mock, unittest

from ..client import RpcClient, RpcClientException, RpcServerException

class FakeSocket():
   def __init__(self):
      self.sent_data = b''
      self.recv_data = b''
      self.response_data = b''

   def sendall(self, data):
      self.sent_data += data
      self.recv_data += self.response_data
      self.response_data = b''

   def recv(self, size):
      if not self.recv_data:
         raise OSError(EAGAIN, os.strerror(EAGAIN))
      chunk = self.recv_data[:size]
      self.recv_data = self.recv_data[size:]
      return chunk

   def settimeout(self, limit):
      pass

   def fileno(self):
      return 1023

class FakeEpoll():
   def __init__(self):
      self.polls = {}

   def register(self, fileno, flags):
      self.polls[fileno] = flags & ~(select.EPOLLERR|select.EPOLLHUP)

   def unregister(self, fileno):
      del self.polls[fileno]

   def poll(self, timeout):
      return list(self.polls.items())

class ClientTest(unittest.TestCase):
   HOST = 'localhost'
   PORT = '12345'

   def _newClient(self):
      client = RpcClient(ClientTest.HOST, ClientTest.PORT)
      client._connectSocket()
      return client

   def testDoCommandData(self):
      with mock.patch('socket.create_connection') as createMock, \
           mock.patch('arista.utils.rpc.client.epoll') as epollMock:
         createMock.side_effect = lambda x: FakeSocket()
         epollMock.side_effect = FakeEpoll
         api = self._newClient()
         api.sock.response_data = b'{"jsonrpc": "2.0", "id": 0, "result": null}'
         api.doCommand('test')
         self.assertEqual(json.loads(api.sock.sent_data.decode('utf-8')),
                          {'jsonrpc': '2.0', 'method': 'test', 'params': None, 'id': 0})

   def testCommandError(self):
      with mock.patch('socket.create_connection') as createMock, \
           mock.patch('arista.utils.rpc.client.epoll') as epollMock:
         createMock.side_effect = lambda x: FakeSocket()
         epollMock.side_effect = FakeEpoll
         api = self._newClient()
         api.sock.response_data = b'{"jsonrpc": "2.0", "id": 0, "error": {"code": -1, "message": "foo"}}'
         with self.assertRaises(RpcServerException):
            api.doCommand('test')

   def testWrongVersion(self):
      with mock.patch('socket.create_connection') as createMock, \
           mock.patch('arista.utils.rpc.client.epoll') as epollMock:
         createMock.side_effect = lambda x: FakeSocket()
         epollMock.side_effect = FakeEpoll
         api = self._newClient()
         api.sock.response_data = b'{"jsonrpc": "3.0", "id": 0, "result": null}'
         with self.assertRaises(RpcClientException):
            api.doCommand('test')

   def testWrongId(self):
      with mock.patch('socket.create_connection') as createMock, \
           mock.patch('arista.utils.rpc.client.epoll') as epollMock:
         createMock.side_effect = lambda x: FakeSocket()
         epollMock.side_effect = FakeEpoll
         api = self._newClient()
         api.sock.response_data = b'{"jsonrpc": "2.0", "id": 1, "result": null}'
         with self.assertRaises(RpcClientException):
            api.doCommand('test')

   def testNoResult(self):
      with mock.patch('socket.create_connection') as createMock, \
           mock.patch('arista.utils.rpc.client.epoll') as epollMock:
         createMock.side_effect = lambda x: FakeSocket()
         epollMock.side_effect = FakeEpoll
         api = self._newClient()
         api.sock.response_data = b'{"jsonrpc": "2.0", "id": 0}'
         with self.assertRaises(RpcClientException):
            api.doCommand('test')

if __name__ == '__main__':
   unittest.main()
