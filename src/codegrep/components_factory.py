from codegrep.AnsiCodeFormatter import AnsiCodeFormatter
from codegrep.config.config import Config
from codegrep.contracts.ICodeParser import ICodeParser
from codegrep.formating.contracts.ISpanHighlighter import ISpanHighlighter
from codegrep.formating.SpanHighlighter import SpanHighlighter
from codegrep.language_detection.LanguageCodeDetector import LanguageCodeDetector
from codegrep.pattern_matching.contracts.IPatternMatcher import IPatternMatcher
from codegrep.pattern_matching.RegexPatternMatcher import RegexPatternMatcher
from codegrep.TreeSitterCodeParser import TreeSitterCodeParser


class ComponentFactory:
    def __init__(self, config: Config) -> None:
        self._config = config

    def create_language_detector(self) -> LanguageCodeDetector:
        return LanguageCodeDetector()

    def create_code_parser(self) -> ICodeParser:
        return TreeSitterCodeParser()

    def create_pattern_matcher(self) -> IPatternMatcher:
        return RegexPatternMatcher()

    def create_span_highlighter(self) -> ISpanHighlighter:
        return SpanHighlighter(self._config)

    def create_code_formatter(self) -> AnsiCodeFormatter:
        return AnsiCodeFormatter(self._config)
