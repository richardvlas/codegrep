from typing import Set

from AnsiCodeFormatter import AnsiCodeFormatter
from contracts.CodeLine import CodeLine
from contracts.ContextConfiguration import ContextConfiguration
from contracts.DisplayConfiguration import DisplayConfiguration
from contracts.SyntaxAnalysisResult import SyntaxAnalysisResult
from formating.SpanHighlighter import SpanHighlighter
from HierarchicalContextExtractor import HierarchicalContextExtractor
from language_detection.LanguageCode import LanguageCode
from language_detection.LanguageCodeDetector import LanguageCodeDetector
from pattern_matching.contracts.models import PatternMatchResult
from pattern_matching.RegexPatternMatcher import RegexPatternMatcher
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

    def __init__(
        self,
        filename: str,
        code: str,
        colors: bool = False,
        verbose: bool = False,
        line_number: bool = False,
        parent_scopes: bool = False,  # called parent_context: bool = False
        child_scopes: bool = False,  # called child_context: bool = False
        last_line: bool = True,
        margin: int = 3,
        mark_lois: bool = True,
        header_max: int = 10,  # max number of header lines to show
        show_top_scope: bool = True,
        loi_pad: int = 1,
    ):
        self._filename = filename
        # self._code = code
        # Trim leading/trailing whitespace from the code to ensure accurate line
        # handling via TreeSitter
        self._code = code.strip()
        self._highlight_spans: dict[int, list[tuple[int, int]]] = {}

        # Step 1. Build configuration objects
        self._display_config = DisplayConfiguration(
            use_color=colors,
            show_line_numbers=line_number,
            mark_lines_of_interest=mark_lois,
            line_of_interest_padding=loi_pad,
            top_margin_lines=margin,
            header_max_lines=header_max,
            show_top_of_file_parent_scope=show_top_scope,
        )
        self._context_config = ContextConfiguration(
            include_parent_context=parent_scopes,
            include_child_context=child_scopes,
            include_last_line=last_line,
            verbose_mode=verbose,
        )

        self._build_dependencies()
        self._prepare_code_analysis()

    def grep(self, search_pattern: str, ignore_case: bool = False) -> Set[int]:
        """Find lines matching the pattern and highlight if color is enabled."""
        result: PatternMatchResult = self._pattern_matcher.match(
            search_pattern, self._lines, ignore_case
        )

        matched_line_numbers = {m.line_number for m in result.matches}
        print(f"Matched lines: {matched_line_numbers}")

        self._lines_of_interest = matched_line_numbers

        if self._display_config.use_color:
            for match in result.matches:
                self._highlight_spans[match.line_number] = match.spans
            self._apply_highlighting()

        return matched_line_numbers

    def get_formatted_output(self) -> str:
        """Return the formatted code output with context (auto-applies context if needed)."""
        if not hasattr(self, "_lines_of_interest_with_context"):
            self._add_context()
        return self._format_output()

    # ============================================================
    # Internal methods
    # ============================================================

    def _add_context(self) -> None:
        """Internal. Expand lines of interest by including parent/child context."""
        self._lines_of_interest_with_context = self._context_extractor.extract_context(
            syntax_result=self._syntax_tree_analysis_result,
            lines_of_interest=self._lines_of_interest,
        )

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
            if not self._display_config.use_color:
                # ensure raw content if no color
                # TODO: Refactor to avoid duplication with _apply_highlighting
                code_line.highlighted_content = code_line.content

        return self._code_formatter.format(
            lines_to_show=self._lines_of_interest_with_context,
            code_lines=self._code_lines,
        )

    def _build_dependencies(self) -> None:
        """Constructs all internal dependencies (parser, matcher, extractor, formatter)."""
        self._language_detector = LanguageCodeDetector()
        self._code_parser = TreeSitterCodeParser()
        self._pattern_matcher = RegexPatternMatcher()
        self._span_highlighter = SpanHighlighter()
        self._syntax_tree_analyzer = SyntaxTreeAnalyzer(verbose=True)
        self._context_extractor = HierarchicalContextExtractor(
            self._context_config, self._display_config
        )
        self._code_formatter = AnsiCodeFormatter(self._display_config)

    def _prepare_code_analysis(self) -> None:
        """
        Perform initial setup: parse code into lines and syntax tree and
        initialize analysis structures.
        """
        language_code: LanguageCode = self._language_detector.detect_language(
            filename=self._filename
        )
        if language_code == LanguageCode.UNKNOWN:
            raise ValueError(f"Could not detect language for file: {self._filename}")
        self._language: LanguageCode = language_code

        self._lines: list[str] = self._code.splitlines()
        print(f"Total lines of code: {len(self._lines)}")

        self._code_lines: list[CodeLine] = [
            CodeLine(line_number=i, content=line) for i, line in enumerate(self._lines)
        ]
        self._lines_of_interest: Set[int] = set()

        self._syntax_tree = self._code_parser.parse(
            code=self._code, language=self._language.value
        )

        self._syntax_tree_analysis_result: SyntaxAnalysisResult = (
            self._syntax_tree_analyzer.analyze(self._syntax_tree.root_node, self._lines)
        )


if __name__ == "__main__":

    # TODO: move somewhere else to top: - This works on cmd but not gitbash
    import colorama

    colorama.init()

    # Read code from a file
    FILE_NAME = "src/codegrep/code_sample.py"
    with open(FILE_NAME, "r") as file:
        code = file.read()

    print(code)

    analyzer = CodeContextAnalyzer(
        filename=FILE_NAME,
        code=code,
        colors=True,
        line_number=True,
        parent_scopes=True,
        child_scopes=True,
        show_top_scope=True,
        margin=3,
        header_max=0,
        loi_pad=1,
        last_line=True,
    )

    SEARCH_PATTERN = "MAX_TITLE_LENGTH"

    lines_of_interest = analyzer.grep(SEARCH_PATTERN)
    print(f"Lines of interest: {sorted(lines_of_interest)}")

    # Debug: Check if highlighting was applied
    for line_idx in lines_of_interest:
        line = analyzer._code_lines[line_idx]
        print(f"Line {line_idx}:")
        print(f"  Content: {repr(line.content)}")
        print(f"  Highlighted: {repr(line.highlighted_content)}")
        print(f"  Is of interest: {line.is_of_interest}")

    formatted_output = analyzer.get_formatted_output()
    print("Formatted Output:")
    print(formatted_output)
