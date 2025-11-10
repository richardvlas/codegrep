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
