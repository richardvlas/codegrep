from config.config import Config
from formating.contracts.color_codes import AnsiBackground
from formating.contracts.ISpanHighlighter import ISpanHighlighter
from pattern_matching.contracts.models import MatchSpan


class SpanHighlighter(ISpanHighlighter):
    def __init__(self, config: Config) -> None:
        self._config = config

    def highlight(self, text: str, spans: list[MatchSpan]) -> str:
        """Highlight specified spans in the given text using ANSI color codes.

        Args:
            text (str): The text to highlight spans in.
            spans (list[MatchSpan]): The list of spans to highlight.
        Returns:
            str: The text with highlighted spans.
        """
        highlighted_text = text
        color_code = AnsiBackground.from_name(self._config.color).value

        # Sort spans in reverse order to avoid messing up indices while replacing
        for span in reversed(spans):
            start, end = span.start, span.end
            highlighted_text = (
                highlighted_text[:start]
                + f"{color_code}{highlighted_text[start:end]}{AnsiBackground.RESET.value}"
                + highlighted_text[end:]
            )
        return highlighted_text
