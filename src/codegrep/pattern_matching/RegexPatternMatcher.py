import re

from pattern_matching.contracts.IPatternMatcher import IPatternMatcher
from pattern_matching.contracts.models import LineMatch, MatchSpan, PatternMatchResult


class RegexPatternMatcher(IPatternMatcher):

    def match(
        self, pattern: str, lines: list[str], ignore_case: bool
    ) -> PatternMatchResult:
        """Match a regex pattern against a list of code lines.

        Args:
            pattern (str): The regex pattern to match.
            lines (list[str]): The list of code lines to search.
            ignore_case (bool): Whether to ignore case when matching.

        Returns:
            PatternMatchResult: The detailed pattern match result.
        """
        flags = re.IGNORECASE if ignore_case else 0
        matches = self._find_matches(pattern, lines, flags)
        return PatternMatchResult(pattern=pattern, matches=matches)

    def _find_matches(
        self, pattern: str, lines: list[str], flags: int
    ) -> list[LineMatch]:
        matches: list[LineMatch] = []
        for i, line in enumerate(lines):
            spans: list[MatchSpan] = [
                MatchSpan(start=match.start(), end=match.end())
                for match in re.finditer(pattern, line, flags)
            ]
            if spans:
                matches.append(LineMatch(line_number=i, spans=spans))
        return matches

    def highlight(
        self, text: str, pattern: str, ignore_case: bool, use_color: bool = True
    ) -> str:
        """Highlight all occurrences of pattern in text.

        Args:
            text (str): The text to highlight matches in.
            pattern (str): The regex pattern to match.
            ignore_case (bool): Whether to ignore case when matching.
            use_color (bool): Whether to use ANSI color codes for highlighting.

        Returns:
            str: The text with highlighted matches (using ANSI codes if use_color=True).
        """
        flags = re.IGNORECASE if ignore_case else 0

        if use_color:
            # Red background with white text for highlighted matches
            def replace_func(match: re.Match[str]) -> str:
                return f"\033[41m\033[37m{match.group(0)}\033[0m"

            return re.sub(pattern, replace_func, text, flags=flags)
        else:
            # No color, just return original text
            return text
