from abc import ABC, abstractmethod

from pattern_matching.contracts.models import MatchSpan


class ISpanHighlighter(ABC):
    @abstractmethod
    def highlight(self, text: str, spans: list[MatchSpan]) -> str:
        """Highlight specified spans in the given text.
        Args:
            text (str): The text to highlight spans in.
            spans (list[MatchSpan]): The list of spans to highlight.
        Returns:
            str: The text with highlighted spans.
        """
        pass
