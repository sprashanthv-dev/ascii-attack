# Singleton inherits from type
# thus making it a metaclass
# Reference : https://stackoverflow.com/questions/100003/what-are-metaclasses-in-python
# Reference : https://www.youtube.com/watch?v=Rm4JP7JfsKY

class Singleton(type):
  # Maintain a dictionary of instances
  # for every class that is a singleton
  _instances = {}
  def __call__(self, *args, **kwds):
    # If no instance of the class exists inside the
    # instances dictionary, create it and return it.
    if self not in self._instances:
      self._instances[self] = super(Singleton, self).__call__(*args, **kwds)
    return self._instances[self]