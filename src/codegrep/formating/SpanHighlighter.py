from formating.contracts.ISpanHighlighter import ISpanHighlighter
from pattern_matching.contracts.models import MatchSpan


class SpanHighlighter(ISpanHighlighter):
    def highlight(self, text: str, spans: list[MatchSpan]) -> str:
        """Highlight specified spans in the given text using ANSI color codes.

        Args:
            text (str): The text to highlight spans in.
            spans (list[MatchSpan]): The list of spans to highlight.
        Returns:
            str: The text with highlighted spans.
        """
        highlighted_text = text

        # Sort spans in reverse order to avoid messing up indices while replacing
        for span in reversed(spans):
            start, end = span.start, span.end
            # Apply ANSI codes for red background and white text
            highlighted_text = (
                highlighted_text[:start]
                + f"\033[41m\033[37m{highlighted_text[start:end]}\033[0m"
                + highlighted_text[end:]
            )
        return highlighted_text
