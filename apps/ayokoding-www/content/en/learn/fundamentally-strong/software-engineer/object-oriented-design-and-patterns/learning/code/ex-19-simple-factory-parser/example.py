"""Example 19: Simple Factory: Centralize Parser Construction."""

from typing import Protocol  # => Protocol declares the shape every parser must match


class Parser(Protocol):  # => the abstraction every concrete parser satisfies
    def parse(self, text: str) -> list[str]:  # => the one method every parser provides
        ...  # => Protocol methods have no body -- a structural contract only


class CsvParser:  # => a concrete parser for comma-separated text
    def parse(self, text: str) -> list[str]:  # => satisfies Parser structurally
        return text.split(",")  # => a real, honest implementation


class JsonParser:  # => a SECOND concrete parser, for a single JSON array of strings
    def parse(self, text: str) -> list[str]:  # => satisfies Parser structurally
        return [
            item.strip().strip('"')
            for item in text.strip("[]").split(",")
            # => trims whitespace THEN quotes -- ["x", "y"] both need both trims
        ]  # => a minimal, dependency-free JSON-array parser


class ParserFactory:  # => centralizes parser CONSTRUCTION in exactly one place
    @staticmethod  # => no instance state needed to build a parser
    def create(extension: str) -> Parser:  # => dispatches by file extension
        if extension == "csv":  # => one branch per KNOWN extension
            return CsvParser()  # => constructs the matching concrete parser
        if extension == "json":  # => a second known extension
            return JsonParser()  # => constructs the matching concrete parser
        raise ValueError(
            f"unknown extension: {extension}"
            # => a clean, specific error -- never a silent None or a cryptic KeyError
        )  # => rejects anything the factory does not recognize


csv_parser: Parser = ParserFactory.create("csv")  # => centralized construction
# => the caller never wrote `CsvParser()` directly -- ParserFactory did that internally
print(csv_parser.parse("a,b,c"))  # => confirms the correct concrete parser was built
# => a fifth file format needs one new branch inside create(), nowhere else
# => Output: ['a', 'b', 'c']
# => `ParserFactory.create()` is the ONE place new extensions get registered
