#Circle class accompanied by property-based tests.
##Unlike unit tests, this test randomly generates many different values to be tested and ensures that edge-cases are covered.
from hypothesis import given, strategies as st
import math

class Circle:
    def __init__(self, radius):
        self.radius = radius
        self.area = math.pi * radius ** 2
        self.circumference = 2 * math.pi * radius



@given(st.floats(min_value=0.1, max_value=1e6))
def test_circle_properties(radius):
    c1 = Circle(radius)
    c2 = Circle(radius * 2)

    assert math.isclose(c2.area, 4 * c1.area, rel_tol=1e-9)

    assert math.isclose(c2.circumference, 2 * c1.circumference, rel_tol=1e-9)
