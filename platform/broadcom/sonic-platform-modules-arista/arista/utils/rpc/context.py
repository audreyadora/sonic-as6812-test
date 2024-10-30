
class ClientContext():
   def __init__(self, peer):
      self.addr = peer[0] if peer is not None else None
      self.port = peer[1] if peer is not None else None

   def __str__(self):
      return f'{self.addr}:{self.port}'

   def slotId(self):
      data = self.addr.split('.')
      if len(data) == 1: # NOTE: IPv6 detected, not supported
         return None
      if data[0] != '127' or data[1] != '100' or data[3] != '1':
         return None
      return int(data[2])

   def localhost(self):
      return self.addr == '127.0.0.1'
