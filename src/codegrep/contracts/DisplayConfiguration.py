from dataclasses import dataclass


@dataclass
class DisplayConfiguration:
    """Configuration for how code should be displayed."""

    use_color: bool = False
    show_line_numbers: bool = False
    mark_lines_of_interest: bool = True
    line_of_interest_padding: int = 1
    top_margin_lines: int = 3
    header_max_lines: int = 10
    show_top_of_file_parent_scope: bool = True
