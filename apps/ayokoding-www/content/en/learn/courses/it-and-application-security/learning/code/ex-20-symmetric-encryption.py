"""Example 20: authenticated symmetric encryption with a maintained library."""

from __future__ import (
    annotations,
)  # => Keeps the example portable across supported Python versions.

from cryptography.fernet import (
    Fernet,
)  # => Vetted authenticated encryption; no homemade cipher.


def round_trip(
    plaintext: bytes,
) -> bytes:  # => Plaintext is a local synthetic value in this demo.
    key = (
        Fernet.generate_key()
    )  # => Fresh random symmetric key stays only in process memory.
    box = Fernet(key)  # => The same secret key encrypts and decrypts this message.
    ciphertext = box.encrypt(
        plaintext
    )  # => Produces confidentiality plus tamper detection.
    return box.decrypt(
        ciphertext
    )  # => Recovery succeeds only for authentic ciphertext.


if __name__ == "__main__":  # => Runs without a service, file, or external host.
    print(
        round_trip(b"synthetic customer note")
    )  # => Expected: original bytes are recovered.
