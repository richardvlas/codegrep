from abc import ABC, abstractmethod

from codegrep.pattern_matching.contracts.models import PatternMatchResult


class IPatternMatcher(ABC):
    """Interface for matching patterns in code."""

    @abstractmethod
    def match(
        self, pattern: str, lines: list[str], ignore_case: bool
    ) -> PatternMatchResult:
        pass
