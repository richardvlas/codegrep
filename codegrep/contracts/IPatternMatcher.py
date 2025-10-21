from abc import ABC, abstractmethod
from typing import List, Set


class IPatternMatcher(ABC):
    """Interface for matching patterns in code."""

    @abstractmethod
    def match(self, pattern: str, lines: List[str], ignore_case: bool) -> Set[int]:
        pass
