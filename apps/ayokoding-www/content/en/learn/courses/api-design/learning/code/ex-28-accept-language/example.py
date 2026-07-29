# pyright: strict
"""Example 28: Accept-Language Selects a Localized Message. (co-21)

`Accept-Language` is content negotiation over LANGUAGE rather than media
type -- the same request path, the same status code, but a different
human-readable string depending on what language the caller asked for.
"""

from dataclasses import dataclass  # => a small typed response record for this example

MESSAGES = {  # => co-21: one message key, two language variants -- the localized payload itself
    "en": "Article created successfully.",  # => the English variant
    "id": "Artikel berhasil dibuat.",  # => the Indonesian variant
}  # => end of MESSAGES


@dataclass  # => co-21: status plus the negotiated, localized body
class Response:  # => co-21: the message text varies, the shape does not
    status: int  # => the HTTP status code -- identical regardless of the chosen language
    body: dict[str, str]  # => the localized message body


def create_article(accept_language: str) -> Response:  # => co-21: negotiation happens on THIS header
    language = accept_language if accept_language in MESSAGES else "en"  # => co-21: "en" is the fallback
    return Response(status=201, body={"message": MESSAGES[language]})  # => same status, localized body


english = create_article("en")  # => request 1: English
print(f"en: {english.body}")  # => Output: {'message': 'Article created successfully.'}

indonesian = create_article("id")  # => request 2: Indonesian, same endpoint, same status
print(f"id: {indonesian.body}")  # => Output: {'message': 'Artikel berhasil dibuat.'}

unknown = create_article("fr")  # => request 3: an UNSUPPORTED language falls back to "en"
# => unknown.status is still 201 -- the fallback affects only the message text, never the outcome
print(f"fr (unsupported, falls back): {unknown.body}")  # => Output: falls back to English message
