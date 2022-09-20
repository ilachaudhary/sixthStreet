import time
class LazyValues(object):
  def __init__(self, **value_fn_dict):
    self.value_fn_dict = value_fn_dict
  
  def __getattr__(self, name):
    if name not in self.value_fn_dict:
      raise AttributeError(f"{name} not in {self.value_fn_dict.keys()}")
    try:
      self.__getattribute__(name)
    except AttributeError:
      value = self.value_fn_dict[name]()
      setattr(self, name, value)
    return self.__getattribute__(name)
