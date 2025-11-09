from typing import Any, List

from contracts.ISyntaxTreeAnalyzer import ISyntaxTreeAnalyzer
from contracts.ScopeHeader import ScopeHeader
from contracts.SyntaxAnalysisResult import SyntaxAnalysisResult


class SyntaxTreeAnalyzer(ISyntaxTreeAnalyzer):

    def __init__(self, verbose: bool):
        self._verbose = verbose

    def analyze(self, root_node: Any, lines: List[str]) -> SyntaxAnalysisResult:
        num_lines = len(lines)
        print(f"Number of lines to analyze: {num_lines}")
        scopes_by_line: List[set[int]] = [set() for _ in range(num_lines)]
        scope_headers: List[List[ScopeHeader]] = [[] for _ in range(num_lines)]
        ast_nodes_by_line: List[List[Any]] = [[] for _ in range(num_lines)]

        for i, line in enumerate(lines):
            print(f"{i}: {line}")

        if self._verbose:
            print(f"Analyzing {len(lines)} lines...")

        self._walk_tree(
            root_node,
            lines,
            0,
            scopes_by_line,
            scope_headers,
            ast_nodes_by_line,
        )

        # print(f"Scopes by line: {scopes_by_line}")
        # print(f"Scope headers: {scope_headers}")

        return SyntaxAnalysisResult(
            scopes_by_line=scopes_by_line,
            scope_headers=scope_headers,
            ast_nodes_by_line=ast_nodes_by_line,
        )

    def _walk_tree(
        self,
        node: Any,
        lines: List[str],
        depth: int,
        scopes_by_line: List[set[int]],
        scope_headers: List[List[ScopeHeader]],
        ast_nodes_by_line: List[List[Any]],
    ) -> tuple[int, int]:
        # just test
        # print(f"node.start_point = {node.start_point}")
        # print(f"node.end_point = {node.end_point}")

        start_line = node.start_point[0]
        end_line = node.end_point[0]
        size = end_line - start_line

        if start_line < len(ast_nodes_by_line):
            ast_nodes_by_line[start_line].append(node)

        if size > 0 and start_line < len(scope_headers):
            scope_headers[start_line].append(
                ScopeHeader(
                    scope_size=size,
                    scope_start_line=start_line,
                    scope_end_line=end_line,
                )
            )

        for i in range(start_line, min(end_line + 1, len(scopes_by_line))):
            scopes_by_line[i].add(start_line)

        if self._verbose and getattr(node, "is_named", False):
            snippet = (
                node.text.splitlines()[0] if hasattr(node, "text") and node.text else ""
            )
            print(
                f"{'   ' * depth}{node.type} {start_line}-{end_line} ({size + 1} lines) {snippet}"
            )

        for child in node.children:
            self._walk_tree(
                child,
                lines,
                depth + 1,
                scopes_by_line,
                scope_headers,
                ast_nodes_by_line,
            )

        return start_line, end_line
