from typing import Any, List

from contracts.ISyntaxTreeAnalyzer import ISyntaxTreeAnalyzer
from contracts.SyntaxAnalysisResult import SyntaxAnalysisResult


class SyntaxTreeAnalyzer(ISyntaxTreeAnalyzer):

    def __init__(self, verbose: bool):
        self._verbose = verbose

    def analyze(self, root_node: Any, lines: List[str]) -> SyntaxAnalysisResult:
        # TODO: Implement the actual analysis logic here.
        scopes_by_line: List[set[int]] = [set() for _ in lines]
        print(f"Scopes by line: {scopes_by_line}")


if __name__ == "__main__":
    analyzer = SyntaxTreeAnalyzer(verbose=True)
    analyzer.analyze(None, ["line 1", "line 2"])
    print("Analysis complete.")
