# pyright: strict
"""Example 29: OAuth 2.0 Authorization Code flow. (co-15)

Model the authorization-code grant in-process: the client redirects to the
auth server, which returns a short-lived CODE; the client exchanges that
code (plus its secret) at the token endpoint for an access token. OAuth 2.0
GRANTS AUTHORIZATION (can you do this?), not authentication. Source: RFC 6749.
"""

from dataclasses import dataclass  # => a small typed record for the token response


@dataclass  # => co-15: the token endpoint's response
class TokenResponse:
    access_token: str  # => the bearer token the client uses against protected resources
    token_type: str  # => always "Bearer" here
    expires_in: int  # => the access token's lifetime in seconds


# A toy auth server: one authorization code, bound to one client + its secret.
AUTH_CODE = "auth-code-abc"  # => the short-lived code the auth server issued
CODE_TO_CLIENT = {AUTH_CODE: ("client-7", "client-secret")}  # => code -> (client_id, client_secret)


def exchange_code(code: str, client_id: str, client_secret: str) -> TokenResponse | str:
    # => co-15: the token endpoint -- exchange a code for an access token
    record = CODE_TO_CLIENT.get(code)  # => look up the code
    if record is None:  # => unknown code -> denied
        return "invalid_grant: unknown code"  # => error
    expected_client, expected_secret = record  # => the client + secret bound to THIS code
    if client_id != expected_client or client_secret != expected_secret:  # => client credentials mismatch
        return "invalid_client: credentials do not match"  # => error
    return TokenResponse(access_token=f"access-{client_id}", token_type="Bearer", expires_in=3600)  # => success


good = exchange_code(AUTH_CODE, "client-7", "client-secret")  # => co-15: correct code + credentials
print(f"valid exchange: {good}")  # => Output: TokenResponse(access-token='access-client-7', ...)

wrong_secret = exchange_code(AUTH_CODE, "client-7", "wrong")  # => wrong secret -> rejected
print(f"wrong secret:   {wrong_secret}")  # => Output: invalid_client error

unknown = exchange_code("bogus-code", "client-7", "client-secret")  # => unknown code -> rejected
print(f"unknown code:   {unknown}")  # => Output: invalid_grant error

assert isinstance(good, TokenResponse) and good.token_type == "Bearer"  # => co-15: code exchanges for a token
assert not isinstance(wrong_secret, TokenResponse)  # => wrong credentials are rejected
