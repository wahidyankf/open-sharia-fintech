# learning/code/ex-48-custom-strategy-composite/test_example.py
"""Example 48: A Custom Composite Strategy."""

# => a custom strategy composes st.integers() draws into a domain-shaped value (co-20)
from hypothesis import given  # => same property-test decorator (co-18)
from hypothesis import strategies as st  # => brings in st.composite, for building a DOMAIN-SPECIFIC strategy (co-20)  # fmt: skip


@st.composite  # => co-20: marks this as a CUSTOM strategy -- draw() pulls from other strategies inside it  # fmt: skip
def rectangles(draw):  # => draw is injected automatically by @st.composite -- not called directly by us  # fmt: skip
    width = draw(st.integers(min_value=1, max_value=1000))  # => a CONSTRAINED sub-strategy: always >= 1  # fmt: skip
    height = draw(st.integers(min_value=1, max_value=1000))  # => a second, independent constrained draw  # fmt: skip
    return (width, height)  # => the DOMAIN OBJECT this strategy produces -- a valid (width, height) pair  # fmt: skip


def area(rect: tuple[int, int]) -> int:  # => the unit under test
    width, height = rect  # => unpacks the domain object built by the composite strategy above  # fmt: skip
    return width * height  # => a plain multiplication


@given(rectangles())  # => co-18: uses the CUSTOM strategy above, not a bare st.integers()  # fmt: skip
def test_generated_rectangles_satisfy_their_own_preconditions(rect: tuple[int, int]) -> None:  # => rect is a (width, height) pair, drawn via rectangles() above  # fmt: skip
    width, height = rect  # => every generated value MUST already satisfy the composite's constraints  # fmt: skip
    assert (
        width >= 1
    )  # => precondition 1, guaranteed by min_value=1 in the composite above
    assert height >= 1  # => precondition 2, guaranteed the same way
    assert area(rect) >= 1  # => a derived invariant: area of two positive integers is always positive  # fmt: skip
