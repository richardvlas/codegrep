from config.importer import import_from_string
from language_detection.LanguageCodeDetector import LanguageCodeDetector

LANGUAGE_DETECTORS: dict[str, str] = {
    "default": "language_detection.LanguageCodeDetector:LanguageCodeDetector",
    # "none": None,
}


class Config:
    def __init__(
        self,
        filename: str,
        code: str,
        colors: bool = False,
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
        # TODO: change to interface that allows custom language detectors
        language_detector: type[LanguageCodeDetector] | str = "default",
    ) -> None:
        self.filename = filename
        # Trim leading/trailing whitespace from the code to ensure accurate line
        # handling via TreeSitter
        # self.code = code.strip()
        self.code = code
        self.colors = colors
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
        # line_of_interest_padding
        self.loi_pad = loi_pad
        # show_top_of_file_parent_scope
        self.show_top_scope = show_top_scope

        self.language_detector = language_detector

        self.loaded = False

    def load(self) -> None:
        """Load or reload configuration if needed."""
        if not self.loaded:

            if isinstance(self.language_detector, str):
                print(f"Loading language detector: {self.language_detector}")
                language_detector_class = import_from_string(
                    LANGUAGE_DETECTORS.get(
                        self.language_detector,
                        self.language_detector,
                    )
                )
                self.language_detector_class = language_detector_class
                print(
                    f"Using language detector: {self.language_detector_class.__name__}"
                )
            else:
                self.language_detector_class = self.language_detector
                print(
                    f"Using language detector: {self.language_detector_class.__name__}"
                )

            print("Configuration loaded.")
            self.loaded = True
