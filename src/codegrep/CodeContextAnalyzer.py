from typing import Set

from .AnsiCodeFormatter import AnsiCodeFormatter
from .config.config import Config
from .contracts.CodeLine import CodeLine
from .contracts.ICodeParser import ICodeParser
from .contracts.SyntaxAnalysisResult import SyntaxAnalysisResult
from .formating.contracts.ISpanHighlighter import ISpanHighlighter
from .HierarchicalContextExtractor import HierarchicalContextExtractor
from .language_detection.LanguageCode import LanguageCode
from .language_detection.LanguageCodeDetector import LanguageCodeDetector
from .pattern_matching.contracts.IPatternMatcher import IPatternMatcher
from .pattern_matching.contracts.models import PatternMatchResult
from .SyntaxTreeAnalyzer import SyntaxTreeAnalyzer


class CodeContextAnalyzer:
    """
    High-level orchestrator for code analysis and formatting.
    Automatically constructs all dependencies internally.

    Users simply instantiate and use it:
        analyzer = CodeContextAnalyzer(config)
        analyzer.grep("def ")
    """

    def __init__(
        self,
        config: Config,
        language_detector: LanguageCodeDetector,
        code_parser: ICodeParser,
        pattern_matcher: IPatternMatcher,
        span_highlighter: ISpanHighlighter,
        code_formatter: AnsiCodeFormatter,
    ) -> None:
        self._config = config
        self._language_detector = language_detector
        self._code_parser = code_parser
        self._pattern_matcher = pattern_matcher
        self._span_highlighter = span_highlighter
        self._code_formatter = code_formatter

        self._syntax_tree_analyzer = SyntaxTreeAnalyzer(verbose=self._config.verbose)
        self._context_extractor = HierarchicalContextExtractor(
            header_max=self._config.header_max,
            child_scopes=self._config.child_scopes,
            last_line=self._config.last_line,
            parent_scopes=self._config.parent_scopes,
            loi_pad=self._config.loi_pad,
            show_top_scope=self._config.show_top_scope,
            margin=self._config.margin,
            verbose=self._config.verbose,
        )

        self._highlight_spans: dict[int, list[tuple[int, int]]] = {}
        self._syntax_tree_analysis_result: SyntaxAnalysisResult | None = None

    def grep(self, search_pattern: str, ignore_case: bool = False) -> Set[int]:
        self._ensure_is_analyzed()

        result: PatternMatchResult = self._pattern_matcher.match(
            search_pattern, self._lines, ignore_case
        )

        matched_line_numbers = {m.line_number for m in result.matches}

        self._lines_of_interest = matched_line_numbers

        if self._config.colors:
            for match in result.matches:
                self._highlight_spans[match.line_number] = match.spans
            self._apply_highlighting()

        return matched_line_numbers

    def get_formatted_output(self) -> str:
        """Return the formatted code output with context (auto-applies context if needed)."""
        if not hasattr(self, "_lines_of_interest_with_context"):
            self._lines_of_interest_with_context = (
                self._context_extractor.extract_context(
                    syntax_result=self._syntax_tree_analysis_result,
                    lines_of_interest=self._lines_of_interest,
                )
            )
        return self._format_output()

    def _apply_highlighting(self) -> None:
        """Internal. Apply syntax highlighting to matched lines."""
        for i, code_line in enumerate(self._code_lines):
            if i in self._highlight_spans:
                spans = self._highlight_spans[i]
                code_line.highlighted_content = self._span_highlighter.highlight(
                    text=code_line.content,
                    spans=spans,
                )
            else:
                code_line.highlighted_content = code_line.content

    def _format_output(self) -> str:
        """Internal. Format the code lines (context + highlighting)."""
        for i, code_line in enumerate(self._code_lines):
            code_line.is_of_interest = i in self._lines_of_interest
            if not self._config.colors:
                # ensure raw content if no color
                # TODO: Refactor to avoid duplication with _apply_highlighting
                code_line.highlighted_content = code_line.content

        return self._code_formatter.format(
            lines_to_show=self._lines_of_interest_with_context,
            code_lines=self._code_lines,
        )

    def _ensure_is_analyzed(self) -> None:
        if self._syntax_tree_analysis_result is None:
            self._perform_syntax_tree_analysis()

    def _perform_syntax_tree_analysis(self) -> None:
        language_code: LanguageCode = self._language_detector.detect_language(
            filename=self._config.filename
        )
        if language_code == LanguageCode.UNKNOWN:
            raise ValueError(
                f"Could not detect language for file: {self._config.filename}"
            )
        self._language: LanguageCode = language_code

        # TODO: move to appropriate place
        code = self._config.code.strip()

        self._lines: list[str] = code.splitlines()
        self._code_lines: list[CodeLine] = [
            CodeLine(line_number=i, content=line) for i, line in enumerate(self._lines)
        ]
        self._lines_of_interest: Set[int] = set()

        self._syntax_tree = self._code_parser.parse(
            code=code, language=self._language.value
        )
        self._syntax_tree_analysis_result = self._syntax_tree_analyzer.analyze(
            self._syntax_tree.root_node, self._lines
        )
