from typing import Any, List, Set

from contracts.SyntaxAnalysisResult import SyntaxAnalysisResult


class HierarchicalContextExtractor:
    """
    Extracts hierarchical code context based on syntax structure
    and user-defined configurations.

    This class is designed to be stateless with respect to code analysis results —
    it uses the SyntaxAnalysisResult per call, while configuration is injected once.
    """

    def __init__(
        self,
        header_max: int = 10,
        child_scopes: bool = True,
        last_line: bool = True,
        parent_scopes: bool = True,
        loi_pad: int = 1,
        show_top_scope: bool = True,
        margin: int = 3,
        verbose: bool = False,
    ) -> None:
        self._header_max_lines = header_max
        self._include_child_context = child_scopes
        self._include_last_line = last_line
        self._include_parent_context = parent_scopes
        self._line_of_interest_padding = loi_pad
        self._show_top_of_file_parent_scope = show_top_scope
        self._top_margin_lines = margin
        self._verbose_mode = verbose

        self._processed_parent_scopes: Set[int] = set()

    # =====================================================================
    # Public API
    # =====================================================================

    def extract_context(
        self,
        syntax_result: SyntaxAnalysisResult,
        lines_of_interest: Set[int],
    ) -> Set[int]:
        """
        Compute a set of line indices that should be displayed, based on:
        - Lines of interest (from grep or analysis)
        - Configured padding, parent, and child context inclusion
        - Scope analysis (from SyntaxTreeAnalyzer)
        """
        if not lines_of_interest:
            return set()

        lines_to_show = set(lines_of_interest)
        self._processed_parent_scopes.clear()

        # Add padding around LOIs
        lines_to_show = self._add_padding(lines_to_show, syntax_result)

        # Add the last line if configured
        if self._include_last_line:
            last_line = len(syntax_result.scopes_by_line) - 1
            if last_line >= 0:
                lines_to_show.add(last_line)
                if self._include_parent_context:
                    self._add_parent_context(last_line, syntax_result, lines_to_show)

        # Include parent and child scopes
        if self._include_parent_context:
            for line in lines_of_interest:
                self._add_parent_context(line, syntax_result, lines_to_show)

        if self._include_child_context:
            for line in lines_of_interest:
                self._add_child_context(line, syntax_result, lines_to_show)

        # Add top-of-file margin
        if self._top_margin_lines:
            lines_to_show.update(range(self._top_margin_lines))

        # Close small one-line gaps
        lines_to_show = self._close_gaps(lines_to_show)

        if self._verbose_mode:
            print(f"[ContextExtractor] Lines of interest: {sorted(lines_of_interest)}")
            print(f"[ContextExtractor] Final lines to show: {sorted(lines_to_show)}")

        return lines_to_show

    # =====================================================================
    # Internal helpers
    # =====================================================================

    def _add_padding(
        self,
        lines: Set[int],
        syntax_result: SyntaxAnalysisResult,
    ) -> Set[int]:
        """Add configurable padding around each line of interest."""
        padded = set(lines)
        padding = self._line_of_interest_padding
        total_lines = len(syntax_result.scopes_by_line)

        for line in list(lines):
            for new_line in range(line - padding, line + padding + 1):
                if 0 <= new_line < total_lines:
                    padded.add(new_line)
        return padded

    def _add_parent_context(
        self,
        line: int,
        syntax_result: SyntaxAnalysisResult,
        lines_to_show: Set[int],
    ) -> None:
        """Add parent scope context for the given line."""
        if line in self._processed_parent_scopes:
            return
        self._processed_parent_scopes.add(line)

        if line >= len(syntax_result.scopes_by_line):
            return

        for scope_start in syntax_result.scopes_by_line[line]:
            if scope_start < len(syntax_result.scope_headers):
                headers = syntax_result.scope_headers[scope_start]
                if not headers:
                    continue

                header = headers[0]
                head_start = header.scope_start_line
                head_end = min(
                    header.scope_end_line,
                    head_start + self._header_max_lines,
                )

                if head_start > 0 or self._show_top_of_file_parent_scope:
                    lines_to_show.update(range(head_start, head_end + 1))

    def _add_child_context(
        self,
        line: int,
        syntax_result: SyntaxAnalysisResult,
        lines_to_show: Set[int],
    ) -> None:
        """Add context lines for child scopes under the given line."""
        if line >= len(syntax_result.ast_nodes_by_line):
            return

        nodes = syntax_result.ast_nodes_by_line[line]
        if not nodes:
            return

        last_line = max(node.end_point[0] for node in nodes)
        scope_size = last_line - line

        # If small scope, include fully
        if scope_size < 5:
            lines_to_show.update(range(line, last_line + 1))
            return

        # Otherwise, selectively add larger child scopes
        children = []
        for node in nodes:
            children.extend(self._collect_children(node))

        children.sort(key=lambda n: n.end_point[0] - n.start_point[0], reverse=True)
        max_to_add = max(min(scope_size * 0.10, 25), 5)
        count_before = len(lines_to_show)

        for child in children:
            if len(lines_to_show) - count_before > max_to_add:
                break
            child_start = child.start_point[0]
            self._add_parent_context(child_start, syntax_result, lines_to_show)

    def _collect_children(self, node: Any) -> List[Any]:
        """Recursively collect all children of a node."""
        result = [node]
        for child in getattr(node, "children", []):
            result.extend(self._collect_children(child))
        return result

    def _close_gaps(self, lines: Set[int]) -> Set[int]:
        """Fill in small one-line gaps to smooth context."""
        closed = set(lines)
        sorted_lines = sorted(lines)

        for i in range(len(sorted_lines) - 1):
            if sorted_lines[i + 1] - sorted_lines[i] == 2:
                closed.add(sorted_lines[i] + 1)

        return closed
