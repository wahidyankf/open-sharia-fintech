# ex-50: isolated Git teaching artifact
from hashlib import sha1


def object_id(payload: bytes) -> str:
    return sha1(b"blob " + str(len(payload)).encode() + b"\\0" + payload).hexdigest()


print(object_id(b"example"))
