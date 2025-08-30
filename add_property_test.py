#Code with an adder function as well as property-based test.
#Unlike unit tests, these test randomly generate many different values to be tested and ensure that edge-cases are covered.
from hypothesis import given
import hypothesis.strategies as st


# adder.py

def add(a, b):
    return a + b




@given(st.integers(), st.integers())
def test_add_commutative(x, y):
        #Property: a + b == b + a
        assert add(x, y) == add(y, x)

@given(st.integers(), st.integers(), st.integers())
def test_add_associative(x, y, z):
        #Property: (a + b) + c = a + (b + c).
        assert add(add(x, y), z) == add(x, add(y, z))