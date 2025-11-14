class Config:
    def __init__(
        self,
        filename: str,
        code: str,
        colors: bool = False,
        color: str = "red",
        verbose: bool = False,
        line_numbers: bool = False,
        parent_scopes: bool = False,  # called parent_context: bool = False
        child_scopes: bool = False,  # called child_context: bool = False
        last_line: bool = True,
        margin: int = 3,
        mark_lois: bool = True,
        header_max: int = 10,  # max number of header lines to show
        show_top_scope: bool = True,
        loi_pad: int = 1,
    ) -> None:
        self.filename = filename
        self.code = code
        self.colors = colors
        self.color = color
        self.verbose = verbose
        self.line_numbers = line_numbers
        # called parent_context: bool = False
        self.parent_scopes = parent_scopes
        # child_context
        self.child_scopes = child_scopes
        self.last_line = last_line
        # top_margin_lines
        self.margin = margin
        # mark_lines_of_interest
        self.mark_lois = mark_lois
        # header_max_lines
        self.header_max = header_max
        # show_top_of_file_parent_scope
        self.show_top_scope = show_top_scope
        # line_of_interest_padding
        self.loi_pad = loi_pad
