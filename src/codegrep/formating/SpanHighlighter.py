from codegrep.config.config import Config
from codegrep.formating.contracts.color_codes import AnsiBackground
from codegrep.formating.contracts.ISpanHighlighter import ISpanHighlighter
from codegrep.pattern_matching.contracts.models import MatchSpan


class SpanHighlighter(ISpanHighlighter):
    def __init__(self, config: Config) -> None:
        self._config: Config = config

    def highlight(self, text: str, spans: list[MatchSpan]) -> str:
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
