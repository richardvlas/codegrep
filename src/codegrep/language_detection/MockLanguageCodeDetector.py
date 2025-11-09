from language_detection.LanguageCode import LanguageCode


class MockLanguageCodeDetector:

    def detect_language(self, filename: str) -> LanguageCode:

        print("MockLanguageCodeDetector: always returning BASH")
        return LanguageCode.BASH
