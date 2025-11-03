from language_detection.LanguageCode import LanguageCode

FILETYPE_TO_LANGUAGE_CODE_MAP: dict[str, LanguageCode] = {
    ".sh": LanguageCode.BASH,
    ".c": LanguageCode.C,
    ".cpp": LanguageCode.CPP,
    ".cs": LanguageCode.CSHARP,
    ".dockerfile": LanguageCode.DOCKERFILE,
    "Dockerfile": LanguageCode.DOCKERFILE,
    ".go": LanguageCode.GO,
    ".java": LanguageCode.JAVA,
    ".js": LanguageCode.JAVASCRIPT,
    ".md": LanguageCode.MARKDOWN,
    ".py": LanguageCode.PYTHON,
    ".php": LanguageCode.PHP,
    ".rb": LanguageCode.RUBY,
    ".rs": LanguageCode.RUST,
    ".ts": LanguageCode.TYPESCRIPT,
    ".yaml": LanguageCode.YAML,
    # "": LanguageCode.UNKNOWN,
}
