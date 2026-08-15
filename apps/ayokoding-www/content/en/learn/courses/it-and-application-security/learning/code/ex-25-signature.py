"""Example 25: sign and verify a message; tampering is rejected."""

from __future__ import annotations  # => Keeps annotations unambiguous.

from cryptography.exceptions import (
    InvalidSignature,
)  # => Verification failure is an expected safe outcome.
from cryptography.hazmat.primitives.asymmetric import (
    ed25519,
)  # => Maintained modern signature primitive.


def verifies(
    message: bytes,
) -> bool:  # => Message is a synthetic audit record in this isolated demo.
    private_key = (
        ed25519.Ed25519PrivateKey.generate()
    )  # => Private key is generated in memory only.
    signature = private_key.sign(
        message
    )  # => Only the private key produces this signature.
    public_key = private_key.public_key()  # => Public key verifies but cannot sign.
    try:  # => Tampering is expected to take the rejection branch.
        public_key.verify(
            signature, message + b"!"
        )  # => Different bytes must not verify.
    except InvalidSignature:  # => Library detected an integrity failure.
        return False  # => Fail closed; never accept a changed message.
    return True  # => This branch would indicate an unexpected verification error.


if __name__ == "__main__":  # => Executes entirely in process.
    print(
        verifies(b"approve synthetic invoice 42")
    )  # => Expected: False for the tampered message.
