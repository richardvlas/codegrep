from typing import Set

from AnsiCodeFormatter import AnsiCodeFormatter
from config.config import Config
from contracts.CodeLine import CodeLine
from contracts.SyntaxAnalysisResult import SyntaxAnalysisResult
from formating.contracts.ISpanHighlighter import ISpanHighlighter
from formating.SpanHighlighter import SpanHighlighter
from HierarchicalContextExtractor import HierarchicalContextExtractor
from language_detection.LanguageCode import LanguageCode
from language_detection.LanguageCodeDetector import LanguageCodeDetector
from pattern_matching.contracts.IPatternMatcher import IPatternMatcher
from pattern_matching.contracts.models import PatternMatchResult
from SyntaxTreeAnalyzer import SyntaxTreeAnalyzer
from TreeSitterCodeParser import TreeSitterCodeParser


class CodeContextAnalyzer:
    """
    High-level orchestrator for code analysis and formatting.
    Automatically constructs all dependencies internally.

    Users simply instantiate and use it:
        analyzer = CodeContextAnalyzer("file.py", code)
        analyzer.grep("def ")
        analyzer.add_context()
        print(analyzer.format())
    """

    def __init__(self, config: Config) -> None:
        self._config = config
        # Trim leading/trailing whitespace from the code to ensure accurate line
        # handling via TreeSitter
        # self._code = code.strip()

        # This was moved to config and _language_detector is created in _analyze_syntax_tree
        # self._language_detector = LanguageCodeDetector()
        # _language_detector should be function rather than class instance?
        # TODO: do the same with the other components?
        # Mostly useful for CodeParser and CodeFormatter?
        #
        self._code_parser = TreeSitterCodeParser()
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
        # self._code_formatter = AnsiCodeFormatter(
        #     colors=self._config.colors,
        #     line_numbers=self._config.line_numbers,
        #     mark_lois=self._config.mark_lois,
        # )

        self._highlight_spans: dict[int, list[tuple[int, int]]] = {}
        self._syntax_tree_analysis_result: SyntaxAnalysisResult | None = None

    def grep(self, search_pattern: str, ignore_case: bool = False) -> Set[int]:
        self._ensure_ready()

        result: PatternMatchResult = self._pattern_matcher.match(
            search_pattern, self._lines, ignore_case
        )

        matched_line_numbers = {m.line_number for m in result.matches}
        print(f"Matched lines: {matched_line_numbers}")

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

    def _resolve_dependencies(self) -> None:
        config = self._config
        if not self._config.loaded:
            config.load()

            # TODO: replace the type with interface that allows custom language detectors
            self._language_detector: LanguageCodeDetector = (
                config.language_detector_class()
            )
            self._pattern_matcher: IPatternMatcher = config.pattern_matcher_class()
            # self._span_highlighter: ISpanHighlighter = SpanHighlighter(config)
            self._span_highlighter: ISpanHighlighter = config.span_highlighter_class(
                config=config
            )
            self._code_formatter = AnsiCodeFormatter(config=config)

    def _ensure_is_analyzed(self) -> None:
        if self._syntax_tree_analysis_result is None:
            self._perform_syntax_tree_analysis()

    def _ensure_ready(self) -> None:
        self._resolve_dependencies()
        self._ensure_is_analyzed()

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


if __name__ == "__main__":

    import time

    # TODO: move somewhere else to top: - This works on cmd but not gitbash
    import colorama
    from language_detection.MockLanguageCodeDetector import MockLanguageCodeDetector

    colorama.init()

    # Read code from a file
    FILE_NAME = "src/codegrep/code_sample.py"
    with open(FILE_NAME, "r") as file:
        code = file.read()

    print(code)

    config = Config(
        filename=FILE_NAME,
        code=code,
        colors=True,
        color="red",
        line_numbers=True,
        parent_scopes=True,
        child_scopes=True,
        show_top_scope=True,
        margin=3,
        header_max=0,
        loi_pad=1,
        last_line=True,
        language_detector="language_detection.MockLanguageCodeDetector:MockLanguageCodeDetector",
        # language_detector=MockLanguageCodeDetector,
        # pattern_matcher="pattern_matching.RegexPatternMatcher:RegexPatternMatcher",
    )

    analyzer = CodeContextAnalyzer(config=config)

    SEARCH_PATTERN = "MAX_TITLE_LENGTH"

    start_time = time.time()
    lines_of_interest = analyzer.grep(SEARCH_PATTERN)
    end_time = time.time()
    print(f"Lines of interest: {sorted(lines_of_interest)}")
    print(f"Time taken for grep: {end_time - start_time:.4f} seconds")

    # Check for second time to test caching
    start_time = time.time()
    lines_of_interest = analyzer.grep(SEARCH_PATTERN)
    end_time = time.time()
    print(f"Lines of interest: {sorted(lines_of_interest)}")
    print(f"Time taken for grep (2nd run): {end_time - start_time:.4f} seconds")

    # Debug: Check if highlighting was applied
    for line_idx in lines_of_interest:
        line = analyzer._code_lines[line_idx]
        print("-" * 40)
        print(f"Line {line_idx}:")
        print(f"  Content: {repr(line.content)}")
        print(f"  Highlighted: {repr(line.highlighted_content)}")
        print(f"  Is of interest: {line.is_of_interest}")
        print("-" * 40)

    formatted_output = analyzer.get_formatted_output()
    print("Formatted Output:")
    print(formatted_output)
