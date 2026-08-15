from typing import Final  # => typed survey fixture

AUGMENTATIONS: Final[set[str]] = {"retrieval", "tools", "memory"}  # => building blocks
assert len(AUGMENTATIONS) == 3  # => all augmentation categories are visible
print("PASS: augmented-llm")  # => credential-free result
