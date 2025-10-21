import re
from typing import List, Set

from contracts.IPatternMatcher import IPatternMatcher


class RegexPatternMatcher(IPatternMatcher):

    def match(self, pattern: str, lines: List[str], ignore_case: bool) -> Set[int]:
        """Match a regex pattern against a list of code lines.

        Args:
            pattern (str): The regex pattern to match.
            lines (List[str]): The list of code lines to search.
            ignore_case (bool): Whether to ignore case when matching.

        Returns:
            Set[int]: A set of line numbers where the pattern matches.
        """
        flags = re.IGNORECASE if ignore_case else 0
        matched_line_numbers = self._find_matching_lines(pattern, lines, flags)
        return matched_line_numbers

    def _find_matching_lines(
        self, pattern: str, lines: List[str], flags: int
    ) -> Set[int]:
        matched_lines: Set[int] = set()
        for i, line in enumerate(lines):
            if re.search(pattern, line, flags):
                matched_lines.add(i)
        return matched_lines


if __name__ == "__main__":
    code_lines = [
        "def my_function():",
        "    print('Hello, World!')",
        "    return True",
        "# This is a comment line comment again",
        "if __name__ == '__main__':",
        "    my_function()",
    ]

    pattern = r"func"
    matcher = RegexPatternMatcher()
    matched_line_numbers = matcher.match(pattern, code_lines, ignore_case=False)
    print(f"Pattern '{pattern}' found in lines: {matched_line_numbers}")
