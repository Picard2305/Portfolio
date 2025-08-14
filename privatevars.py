#Allows for true private variables in Python
import weakref
import inspect

# ------------------------
# Private class decorator
# ------------------------
def PrivateClass(cls):
    _inst_storage = weakref.WeakKeyDictionary()
    _class_storage = getattr(cls, "__class_private__", {}) or {}

    if hasattr(cls, "__class_private__"):
        try: delattr(cls, "__class_private__")
        except Exception: pass

    # Determines if caller is allowed to access
    def _who_called_exact_class(expected_cls):
        f = inspect.currentframe().f_back
        loc = f.f_locals
        caller_self = loc.get("self", None)
        caller_cls_local = loc.get("cls", None)
        if caller_self is not None:
            return isinstance(caller_self, expected_cls)  # <-- allow subclasses
        if caller_cls_local is not None:
            return issubclass(caller_cls_local, expected_cls)  # <-- allow subclass classmethods
        return False

    # Instance-level private
    def _get_private(self):
        if not _who_called_exact_class(cls):
            raise PermissionError(f"Access to instance-private vars of {cls.__name__} denied")
        if self not in _inst_storage:
            _inst_storage[self] = {}
        return _inst_storage[self]

    # Class-level private
    def _get_class_private_inner(_cls):
        if _cls is not cls:
            raise PermissionError(f"Access to class-private vars of {cls.__name__} denied")
        return _class_storage

    cls._get_private = _get_private
    cls._get_class_private = classmethod(_get_class_private_inner)
    return cls

# ------------------------
# Helpers
# ------------------------
def pv_class_collect(existing, name, value):
    d = existing if isinstance(existing, dict) else {}
    d[name] = value
    return d

def priv(self, name, value):
    self._get_private()[name] = value
    return value

def class_priv(cls, name, value):
    cls._get_class_private()[name] = value
    return value
