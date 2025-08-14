import weakref
import inspect

def PrivateClass(cls):
    """Decorator to enable C++-style private instance and class variables."""
    # Storage
    _inst_storage = weakref.WeakKeyDictionary()
    _class_storage = getattr(cls, "__class_private__", {}) or {}

    if hasattr(cls, "__class_private__"):
        delattr(cls, "__class_private__")

    # Instance-private accessor
    def _get_private(self, _constructor=False):
        """Access instance-private variables."""
        f = inspect.currentframe().f_back
        caller_self = f.f_locals.get("self", None)

        if _constructor:
            # Allow subclass constructor
            if not isinstance(self, cls):
                raise PermissionError(f"Access to instance-private vars of {cls.__name__} denied")
        else:
            # Only allow exact class instances
            if type(self) is not cls:
                raise PermissionError(f"Access to instance-private vars of {cls.__name__} denied")

        if self not in _inst_storage:
            _inst_storage[self] = {}
        return _inst_storage[self]

    # Class-private accessor
    def _get_class_private(_cls):
        if _cls is not cls:
            raise PermissionError(f"Access to class-private vars of {cls.__name__} denied")
        return _class_storage

    # Attach sugar methods
    cls._get_private = _get_private
    cls._get_class_private = classmethod(_get_class_private)
    return cls

# Helpers for sugar syntax
def priv(self, name, value):
    """Set an instance-private variable (constructor only)."""
    self._get_private(_constructor=True)[name] = value
    return value

def class_priv(cls, name, value):
    """Set a class-private variable."""
    cls._get_class_private()[name] = value
    return value

def pv_class_collect(existing, name, value):
    """Collect class-private variables easily."""
    d = existing if isinstance(existing, dict) else {}
    d[name] = value
    return d

