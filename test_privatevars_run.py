from privatevars import PrivateClass, priv, class_priv, pv_class_collect

# ------------------------
# Test classes
# ------------------------
@PrivateClass
class TestClass:
    __class_private__ = pv_class_collect(None, "CLASS_SECRET", 42)

    def __init__(self, value):
        priv(self, "value", value)

    def get_value(self):
        return self._get_private()["value"]

    @classmethod
    def get_class_secret(cls):
        return cls._get_class_private()["CLASS_SECRET"]

class SubTestClass(TestClass):
    def __init__(self, value, extra):
        super().__init__(value)
        priv(self, "extra", extra)

    def get_extra(self):
        return self._get_private()["extra"]

    @classmethod
    def set_class_secret(cls, new_secret):
        # Attempt to modify parent class-private variable
        try:
            class_priv(cls, "CLASS_SECRET", new_secret)
        except PermissionError:
            return "Blocked"
        return "Changed"

# ------------------------
# Instance-level tests
# ------------------------
def test_instance_private_access():
    obj = TestClass(10)
    assert obj.get_value() == 10
    priv(obj, "value", obj.get_value() + 5)
    assert obj.get_value() == 15

def test_instance_private_isolation():
    a = TestClass(1)
    b = TestClass(2)
    # Each instance has its own private storage
    assert a.get_value() != b.get_value()
    # Direct access of another instance's private should not exist
    try:
        b._get_private()["value"] = 999  # simulate illegal modification
    except PermissionError:
        pass
    assert a.get_value() == 1

def test_instance_private_subclass():
    sub = SubTestClass(5, 99)
    # Subclass can access its own instance-private variable
    assert sub.get_extra() == 99
    priv(sub, "extra", 123)
    assert sub.get_extra() == 123
    # Subclass also has parent instance-private variable for this instance
    assert sub.get_value() == 5

# ------------------------
# Class-level tests
# ------------------------
def test_class_private_access():
    assert TestClass.get_class_secret() == 42

def test_class_private_blocked():
    result = SubTestClass.set_class_secret(100)
    assert result == "Blocked"
    assert TestClass.get_class_secret() == 42  # parent remains unchanged

# ------------------------
# Run all tests
# ------------------------
if __name__ == "__main__":
    test_instance_private_access()
    test_instance_private_isolation()
    test_instance_private_subclass()
    test_class_private_access()
    test_class_private_blocked()
    print("All tests passed successfully!")
