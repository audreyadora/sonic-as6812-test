
class HwDesc(object):

   OID_FIELD = None

   def __init__(self, **kwargs):
      self.setAttrs(**kwargs)

   @classmethod
   def __lid2oid__(cls, lid):
      return lid

   @classmethod
   def __oid2lid__(cls, oid):
      return oid

   def __getoid__(self):
      if self.OID_FIELD is None:
         raise NotImplementedError
      return self.__lid2oid__(getattr(self, self.OID_FIELD))

   def __setoid__(self, oid):
       setattr(self, self.OID_FIELD, self.__oid2lid__(oid))

   def setAttrs(self, **kwargs):
      for key, value in kwargs.items():
         setattr(self, key, value)

   def __diag__(self, ctx):
      return { k : v.__diag__(ctx) if isinstance(v, HwDesc) else v
               for k, v in self.__dict__.items() }
