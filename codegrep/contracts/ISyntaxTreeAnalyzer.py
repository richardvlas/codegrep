from abc import ABC, abstractmethod
from typing import Any, List

from contracts.SyntaxAnalysisResult import SyntaxAnalysisResult


class ISyntaxTreeAnalyzer(ABC):
    """Interface for analyzing syntax trees of code."""

    @abstractmethod
    def analyze(self, root_node: Any, lines: List[str]) -> SyntaxAnalysisResult:
        pass
