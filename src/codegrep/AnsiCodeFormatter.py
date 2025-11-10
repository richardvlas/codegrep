from typing import List, Set

from config.config import Config
from contracts.CodeLine import CodeLine
from formating.contracts.color_codes import AnsiForeground


class AnsiCodeFormatter:
    """
    Formats code lines for console display using ANSI color codes and line numbers.

    - Shows only selected lines (based on extracted context)
    - Adds markers for lines of interest
    - Optionally highlights matches and adds ellipses for skipped lines
    """

    def __init__(self, config: Config) -> None:
        self._config = config

    def format(self, lines_to_show: Set[int], code_lines: List[CodeLine]) -> str:
        """
        Format a subset of lines for display, including color, numbering, and markers.
        """
        if not lines_to_show or not code_lines:
            return ""

        lines_to_show_sorted = sorted(lines_to_show)
        output_lines: List[str] = []
        last_shown = -2  # Tracks previous line to decide when to insert "⋮"

        if self._config.colors:
            output_lines.append(AnsiForeground.RESET.value)  # Reset ANSI state at start

        for line_index in lines_to_show_sorted:
            if line_index >= len(code_lines):
                continue

            # Add ellipsis (⋮) between non-contiguous lines
            if line_index > last_shown + 1:
                gap_marker = "⋮"
                if self._config.line_numbers:
                    output_lines.append(f"   {gap_marker}")
                else:
                    output_lines.append(gap_marker)

            formatted = self._format_single_line(code_lines[line_index])
            output_lines.append(formatted)
            last_shown = line_index

        # Reset color at the end (safe for terminal output)
        if self._config.colors:
            # output_lines.append("\033[0m")
            output_lines.append(AnsiForeground.RESET.value)

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
        if self._config.line_numbers:
            formatted_line = f"{code_line.line_number + 1:3} {formatted_line}"

        return formatted_line

    def _get_marker(self, code_line: CodeLine) -> str:
        """
        Determine the left-side marker (e.g., █ for lines of interest or │ otherwise).
        """
        color_code = AnsiForeground.from_name(self._config.color).value
        # TODO: is mark_lines_of_interest needed here? Should it always mark lines
        # of interest if is_of_interest is set?
        if code_line.is_of_interest and self._config.mark_lois:
            marker = "█"
            if self._config.colors:
                # return f"\033[31m{marker}\033[0m"
                return f"{color_code}{marker}{AnsiForeground.RESET.value}"
            return marker
        else:
            return "│"
