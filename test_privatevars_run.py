#Test file for privatevars.py
from privatevars import PrivateClass, priv, class_priv, pv_class_collect

# ----------------------------
# Test classes
# ----------------------------

@PrivateClass
class TestClass:
    __class_private__ = pv_class_collect(None, "CLASS_VAR", 42)

    def __init__(self, value):
        priv(self, "value", value)

    def get_value(self):
        return self._get_private()["value"]

    @classmethod
    def get_class_var(cls):
        return cls._get_class_private()["CLASS_VAR"]

@PrivateClass
class SubTestClass(TestClass):
    def __init__(self, value):
        super().__init__(value)
        priv(self, "sub_value", value * 2)

    def get_sub_value(self):
        return self._get_private()["sub_value"]

# ----------------------------
# Test functions
# ----------------------------

def test_instance_private_access():
    obj = TestClass(10)
    assert obj.get_value() == 10
    print("test_instance_private_access passed")

def test_instance_private_blocked():
    sub = SubTestClass(5)
    try:
        # Should raise PermissionError due to C++-style privacy
        sub._get_private()["value"]
        print("ERROR: SubTestClass accessed parent instance-private vars")
    except PermissionError:
        print("test_instance_private_blocked passed")

def test_class_private_access():
    assert TestClass.get_class_var() == 42
    print("test_class_private_access passed")

def test_class_private_blocked():
    sub = SubTestClass(1)
    try:
        # Should raise PermissionError
        sub._get_class_private()
        print("ERROR: SubTestClass accessed parent class-private vars")
    except PermissionError:
        print("test_class_private_blocked passed")

def test_helpers():
    obj = TestClass(7)
    # Instance-private helper
    priv(obj, "new_val", 99)
    assert obj._get_private()["new_val"] == 99

    # Class-private helper
    class_priv(TestClass, "NEW_CLASS_VAR", 100)
    assert TestClass._get_class_private()["NEW_CLASS_VAR"] == 100
    print("test_helpers passed")

# ----------------------------
# Run all tests
# ----------------------------

if __name__ == "__main__":
    test_instance_private_access()
    test_instance_private_blocked()
    test_class_private_access()
    test_class_private_blocked()
    test_helpers()
    print("All tests passed!")
