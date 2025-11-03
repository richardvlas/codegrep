from dataclasses import dataclass


@dataclass
class ScopeHeader:
    scope_size: int
    scope_start_line: int
    scope_end_line: int
