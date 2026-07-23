"""Example 1: Split a God Class by Responsibility."""


class DataParser:  # => the ONLY class that turns raw text into structured rows
    def parse(self, raw: str) -> list[str]:  # => defines the parse() method
        return [
            line.strip()  # => transformation applied to every kept line
            for line in raw.splitlines()  # => splits the raw string on newlines first
            if line.strip()
            # => splits on newlines, trims whitespace, drops blank lines
        ]  # => splits and trims non-blank lines


class ReportFormatter:  # => the ONLY class that turns rows into a display string
    def format(self, rows: list[str]) -> str:  # => defines the format() method
        return "\n".join(
            f"- {row}"  # => the format applied to every row, unconditionally
            for row in rows  # => iterates the caller-supplied rows in order
            # => prefixes every row with a bullet marker, nothing else
        )  # => bullets each row, unrelated to parsing or saving


class ReportWriter:  # => the ONLY class that persists a finished report
    def save(
        self,
        report: str,
        sink: list[str],
        # => sink is a real parameter here, standing in for a real file handle
    ) -> None:  # => sink simulates a file: an in-memory list
        sink.append(report)  # => the sole write path -- no parsing or formatting here


raw_input: str = "alice\n\nbob\ncarol\n"  # => sample raw data, includes a blank line
parser: DataParser = DataParser()  # => constructs parser
formatter: ReportFormatter = ReportFormatter()  # => constructs formatter
writer: ReportWriter = ReportWriter()  # => constructs writer
# => three independent collaborators -- none of them knows the other two exist

rows: list[str] = parser.parse(raw_input)  # => rows is ["alice", "bob", "carol"]
report: str = formatter.format(rows)  # => report is "- alice\n- bob\n- carol"
saved_files: list[str] = []  # => the in-memory "filesystem" ReportWriter appends to
writer.save(report, saved_files)  # => the ONLY line in this program that mutates it
# => a real deployment would swap ReportWriter's sink for an actual open file

print(report)  # => confirms the parse -> format -> save pipeline produced this text
# => Output: - alice
# => - bob
# => - carol
# => Each class changes for exactly one reason: parsing rules, display formatting, or storage -- never more than one
