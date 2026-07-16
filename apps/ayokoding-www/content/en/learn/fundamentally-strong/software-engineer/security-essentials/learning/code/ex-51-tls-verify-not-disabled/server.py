# learning/code/ex-51-tls-verify-not-disabled/server.py
"""Example 51: a real local HTTPS server backed by a genuinely self-signed cert (co-18)."""

from __future__ import (
    annotations,
)  # => DD-39 hygiene -- unrelated to the TLS-verification issue itself

import datetime  # => co-18: real NotBefore/NotAfter validity window for the self-signed cert
import ipaddress  # => co-18: the cert's SAN must cover the real IP requests.py connects to (127.0.0.1)
import os  # => co-18: writes the real cert/key PEM files this example's client half reads
import ssl  # => co-18: wraps the plain HTTP server socket in a REAL TLS context
from http.server import (
    BaseHTTPRequestHandler,
    HTTPServer,
)  # => co-18: stdlib -- no extra web framework needed here

from cryptography import (
    x509,
)  # => co-18: builds a REAL X.509 certificate, not a fabricated string
from cryptography.hazmat.primitives import (
    hashes,
    serialization,
)  # => co-18: real signing hash + PEM serialization
from cryptography.hazmat.primitives.asymmetric import (
    rsa,
)  # => co-18: generates a REAL RSA key pair for the cert
from cryptography.x509.oid import (
    NameOID,
)  # => co-18: standard X.509 subject-name field identifiers

CERT_PATH = os.path.join(
    os.path.dirname(__file__), "selfsigned.crt"
)  # => co-18: written once, reused by both runs
KEY_PATH = os.path.join(
    os.path.dirname(__file__), "selfsigned.key"
)  # => co-18: the matching REAL private key


def generate_self_signed_cert() -> (
    None
):  # => co-18: creates a genuinely self-signed cert -- issuer == subject
    key = rsa.generate_private_key(
        public_exponent=65537, key_size=2048
    )  # => co-18: a real 2048-bit RSA key pair
    subject = issuer = x509.Name(
        [x509.NameAttribute(NameOID.COMMON_NAME, "127.0.0.1")]
    )  # => co-18: self-signed: same
    now = datetime.datetime.now(
        datetime.timezone.utc
    )  # => co-18: real wall-clock UTC time, taken once
    cert = (  # => co-18: every field below is REAL, cryptography-library-constructed X.509 data
        x509.CertificateBuilder()
        .subject_name(
            subject
        )  # => co-18: who this cert claims to identify -- 127.0.0.1
        .issuer_name(
            issuer
        )  # => co-18: SAME as subject -- this IS what "self-signed" means structurally
        .public_key(
            key.public_key()
        )  # => co-18: the real public half of the key pair generated above
        .serial_number(
            x509.random_serial_number()
        )  # => co-18: a real, random serial -- required by the X.509 spec
        .not_valid_before(
            now - datetime.timedelta(days=1)
        )  # => co-18: real validity window start
        .not_valid_after(
            now + datetime.timedelta(days=1)
        )  # => co-18: real validity window end -- short-lived demo cert
        .add_extension(  # => co-18: SAN must list 127.0.0.1 or hostname verification fails for an UNRELATED reason
            x509.SubjectAlternativeName(
                [x509.IPAddress(ipaddress.ip_address("127.0.0.1"))]
            ),
            critical=False,
        )
        .sign(
            key, hashes.SHA256()
        )  # => co-18: the cert signs ITSELF with its own private key -- no real CA involved
    )
    with open(
        CERT_PATH, "wb"
    ) as f:  # => co-18: writes the real PEM-encoded certificate to disk
        f.write(
            cert.public_bytes(serialization.Encoding.PEM)
        )  # => co-18: standard PEM cert format
    with open(
        KEY_PATH, "wb"
    ) as f:  # => co-18: writes the real PEM-encoded private key to disk
        f.write(
            key.private_bytes(
                serialization.Encoding.PEM,
                serialization.PrivateFormat.PKCS8,
                serialization.NoEncryption(),
            )
        )


class Handler(
    BaseHTTPRequestHandler
):  # => co-18: the SAME handler serves every request, over a real TLS socket
    def do_GET(
        self,
    ) -> None:  # => co-18: real stdlib HTTP handler -- runs only after the TLS handshake completes
        self.send_response(
            200
        )  # => co-18: a real 200 -- reaching this line already proves TLS negotiation succeeded
        self.send_header(
            "Content-Type", "text/plain"
        )  # => co-18: a real response header
        self.end_headers()  # => co-18: finalizes the real HTTP response headers
        self.wfile.write(
            b"reached over a real (self-signed) TLS connection\n"
        )  # => co-18: real response body bytes

    def log_message(
        self, format: str, *args: object
    ) -> None:  # => co-18: silences BaseHTTPRequestHandler's default stderr spam
        return None  # => co-18: keeps this example's captured output limited to what exploit_and_fix.py prints


if (
    __name__ == "__main__"
):  # => co-18: only runs when launched directly, e.g. `python3 server.py &`
    generate_self_signed_cert()  # => co-18: creates real cert.pem/key.pem before the TLS listener starts
    context = ssl.SSLContext(
        ssl.PROTOCOL_TLS_SERVER
    )  # => co-18: a real server-side TLS context, TLS 1.2+ by default
    context.load_cert_chain(
        certfile=CERT_PATH, keyfile=KEY_PATH
    )  # => co-18: loads the REAL self-signed cert/key pair
    httpd = HTTPServer(
        ("127.0.0.1", 5051), Handler
    )  # => co-18: localhost-only, fixed port -- exploit_and_fix.py targets this
    httpd.socket = context.wrap_socket(
        httpd.socket, server_side=True
    )  # => co-18: wraps the plain socket in REAL TLS
    httpd.serve_forever()  # => co-18: blocks forever, serving real HTTPS requests until killed
