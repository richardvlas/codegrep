from typing import List, Set

from contracts.CodeLine import CodeLine


class AnsiCodeFormatter:
    """
    Formats code lines for console display using ANSI color codes and line numbers.

    - Shows only selected lines (based on extracted context)
    - Adds markers for lines of interest
    - Optionally highlights matches and adds ellipses for skipped lines
    """

    def __init__(
        self,
        colors: bool = False,
        line_numbers: bool = False,
        mark_lois: bool = True,
    ):
        self._use_color = colors
        self._show_line_numbers = line_numbers
        self._mark_lines_of_interest = mark_lois

    # =====================================================================
    # Public API
    # =====================================================================

    def format(self, lines_to_show: Set[int], code_lines: List[CodeLine]) -> str:
        """
        Format a subset of lines for display, including color, numbering, and markers.
        """
        if not lines_to_show or not code_lines:
            return ""

        lines_to_show_sorted = sorted(lines_to_show)
        output_lines: List[str] = []
        last_shown = -2  # Tracks previous line to decide when to insert "⋮"

        if self._use_color:
            output_lines.append("\033[0m")  # Reset ANSI state at start

        for line_index in lines_to_show_sorted:
            if line_index >= len(code_lines):
                continue

            # Add ellipsis (⋮) between non-contiguous lines
            if line_index > last_shown + 1:
                gap_marker = "⋮"
                if self._show_line_numbers:
                    output_lines.append(f"   {gap_marker}")
                else:
                    output_lines.append(gap_marker)

            formatted = self._format_single_line(code_lines[line_index])
            output_lines.append(formatted)
            last_shown = line_index

        # Reset color at the end (safe for terminal output)
        if self._use_color:
            output_lines.append("\033[0m")

        return "\n".join(output_lines)

    # =====================================================================
    # Internal helpers
    # =====================================================================

    def _format_single_line(self, code_line: CodeLine) -> str:
        """
        Format a single line of code with markers, highlighting, and numbering.
        """
        marker = self._get_marker(code_line)
        content = code_line.highlighted_content or code_line.content

        # Combine marker and code text
        formatted_line = f"{marker} {content}"

        # Optionally add line numbers
        if self._show_line_numbers:
            formatted_line = f"{code_line.line_number + 1:3} {formatted_line}"

        return formatted_line

    def _get_marker(self, code_line: CodeLine) -> str:
        """
        Determine the left-side marker (e.g., █ for lines of interest or │ otherwise).
        """
        # TODO: is mark_lines_of_interest needed here? Should it always mark lines
        # of interest if is_of_interest is set?
        if code_line.is_of_interest and self._mark_lines_of_interest:
            marker = "█"
            if self._use_color:
                # Red for lines of interest
                return f"\033[31m{marker}\033[0m"
            return marker
        else:
            return "│"
