from dataclasses import dataclass
from typing import Any, List, Set

from contracts.ScopeHeader import ScopeHeader


@dataclass
class SyntaxAnalysisResult:
    # For each line, which scopes (by start line) cover this line?
    scopes_by_line: List[Set[int]]
    # For each line, the headers (with their size/start/end) that begin on that line
    scope_headers: List[List[ScopeHeader]]
    # For each line, the AST nodes that start at this line
    ast_nodes_by_line: List[List[Any]]
