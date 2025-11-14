from codegrep.language_detection.FileType import FileType
from codegrep.language_detection.FILETYPE_TO_LANGUAGE_CODE_MAP import (
    FILETYPE_TO_LANGUAGE_CODE_MAP,
)
from codegrep.language_detection.LanguageCode import LanguageCode


class LanguageCodeDetector:

    _FILETYPE_TO_LANGUAGE_MAP: dict[str, LanguageCode] = FILETYPE_TO_LANGUAGE_CODE_MAP

    def detect_language(self, filename: str) -> LanguageCode:

        file_type: FileType = FileType.from_filename(filename)
        return self._FILETYPE_TO_LANGUAGE_MAP.get(file_type.name, LanguageCode.UNKNOWN)
