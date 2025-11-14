from codegrep.language_detection.LanguageCode import LanguageCode

FILETYPE_TO_LANGUAGE_CODE_MAP: dict[str, LanguageCode] = {
    ".sh": LanguageCode.BASH,
    ".c": LanguageCode.C,
    ".cpp": LanguageCode.CPP,
    ".cs": LanguageCode.CSHARP,
    ".csv": LanguageCode.CSV,
    ".dockerfile": LanguageCode.DOCKERFILE,
    "Dockerfile": LanguageCode.DOCKERFILE,
    ".go": LanguageCode.GO,
    # TODO: Add other java related extensions
    ".java": LanguageCode.JAVA,
    ".js": LanguageCode.JAVASCRIPT,
    ".md": LanguageCode.MARKDOWN,
    ".py": LanguageCode.PYTHON,
    ".php": LanguageCode.PHP,
    ".rb": LanguageCode.RUBY,
    ".rs": LanguageCode.RUST,
    ".toml": LanguageCode.TOML,
    ".ts": LanguageCode.TYPESCRIPT,
    ".txt": LanguageCode.TXT,
    ".yaml": LanguageCode.YAML,
    # "": LanguageCode.UNKNOWN,
}
