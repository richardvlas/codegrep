from language_detection.FileType import FileType
from language_detection.FILETYPE_TO_LANGUAGE_CODE_MAP import (
    FILETYPE_TO_LANGUAGE_CODE_MAP,
)
from language_detection.LanguageCode import LanguageCode


class LanguageCodeDetector:

    _FILETYPE_TO_LANGUAGE_MAP: dict[str, LanguageCode] = FILETYPE_TO_LANGUAGE_CODE_MAP

    def detect_language(self, filename: str) -> LanguageCode:

        file_type: FileType = FileType.from_filename(filename)
        return self._FILETYPE_TO_LANGUAGE_MAP.get(file_type.name, LanguageCode.UNKNOWN)


if __name__ == "__main__":
    detector = LanguageCodeDetector()
    filenames = [
        "script.sh",
        "program.c",
        "application.cpp",
        "website.js",
        "Dockerfile",
        "main.go",
        "README.md",
        "unknownfile.xyz",
    ]
    for fname in filenames:
        lang_code = detector.detect_language(fname)
        print(f"Filename: {fname}, Detected Language: {lang_code.value}")
