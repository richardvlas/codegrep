# from codegrep import CodeGrep
from .AnsiCodeFormatter import AnsiCodeFormatter
from .CodeContextAnalyzer import CodeContextAnalyzer
from .components_factory import ComponentFactory
from .config.config import Config
from .contracts.ICodeParser import ICodeParser
from .formating.contracts.ISpanHighlighter import ISpanHighlighter
from .language_detection.LanguageCodeDetector import LanguageCodeDetector
from .pattern_matching.contracts.IPatternMatcher import IPatternMatcher

# config = Config(
#     filename="example.py",
#     code="def foo(): pass",
#     color="green",
# )
# code_grep = CodeGrep(config)
# result = code_grep.analyze()
# print(result)


class Application:
    """Top-level composition root that wires all dependencies."""

    def __init__(self, config: Config) -> None:
        component_factory = ComponentFactory(config)

        # Build dependencies using the factory
        self.language_detector: LanguageCodeDetector = (
            component_factory.create_language_detector()
        )
        self.code_parser: ICodeParser = component_factory.create_code_parser()
        self.pattern_matcher: IPatternMatcher = (
            component_factory.create_pattern_matcher()
        )
        self.span_highlighter: ISpanHighlighter = (
            component_factory.create_span_highlighter()
        )
        self.code_formatter: AnsiCodeFormatter = (
            component_factory.create_code_formatter()
        )

        self._analyzer = CodeContextAnalyzer(
            config=config,
            language_detector=self.language_detector,
            code_parser=self.code_parser,
            pattern_matcher=self.pattern_matcher,
            span_highlighter=self.span_highlighter,
            code_formatter=self.code_formatter,
        )

    def run(self, search_pattern: str, ignore_case: bool = False) -> str:
        """Run the application with the given search pattern."""
        # TODO: result should be reused in get_formatted_output or handle differently
        result = self._analyzer.grep(search_pattern, ignore_case)
        return self._analyzer.get_formatted_output()


if __name__ == "__main__":
    import time

    # TODO: move somewhere else to top: - This works on cmd but not gitbash
    import colorama

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
    )

    application = Application(config=config)

    SEARCH_PATTERN = "MAX_TITLE_LENGTH"

    start_time = time.time()
    result = application.run(SEARCH_PATTERN)
    end_time = time.time()
    print(f"Result:\n{result}")
    print(f"Time taken for grep: {end_time - start_time:.4f} seconds")

    # one more time to test caching
    start_time = time.time()
    result = application.run(SEARCH_PATTERN)
    end_time = time.time()
    print(f"Result:\n{result}")
    print(f"Time taken for grep (2nd run): {end_time - start_time:.4f} seconds")
