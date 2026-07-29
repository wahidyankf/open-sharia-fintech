"""Example 55: Pydantic Computed Fields.

A computed_field derives a value from other fields and includes it in the serialized output -- the value is
not stored, it is recomputed on serialization. Run: python3 example.py. (co-12, co-14)
"""

from pydantic import BaseModel, computed_field


class Rectangle(BaseModel):  # => a model with two stored fields and one DERIVED field (co-12)
    width: float  # => a stored input
    height: float  # => a stored input

    @computed_field  # => included in model_dump() output, but NOT a stored field (co-14)
    @property
    def area(self) -> float:  # => derived from width + height on every serialization
        return self.width * self.height  # => recomputed, never stored


def main() -> None:  # => demonstrates the computed field appearing in the output
    rect = Rectangle(width=3.0, height=4.0)  # => only width + height are inputs
    dumped = rect.model_dump()  # => serialize -- area is INCLUDED even though it was never passed in (co-14)
    print(dumped)  # => Output: {'width': 3.0, 'height': 4.0, 'area': 12.0}


if __name__ == "__main__":  # => run directly
    main()
