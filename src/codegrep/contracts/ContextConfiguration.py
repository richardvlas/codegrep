from dataclasses import dataclass


@dataclass
class ContextConfiguration:
    """Configuration for context extraction."""

    include_parent_context: bool = True
    include_child_context: bool = True
    include_last_line: bool = True
    verbose_mode: bool = False
