from enum import Enum


class LanguageCode(Enum):
    BASH = "bash"
    C = "c"
    CPP = "cpp"
    CSHARP = "csharp"
    DOCKERFILE = "dockerfile"
    GO = "go"
    JAVA = "java"
    JAVASCRIPT = "javascript"
    MARKDOWN = "markdown"
    PYTHON = "python"
    PHP = "php"
    RUBY = "ruby"
    RUST = "rust"
    TYPESCRIPT = "typescript"
    YAML = "yaml"
    UNKNOWN = "unknown"


MAP_FILETYPE_TO_LANGUAGE: dict[str, LanguageCode] = {
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
    "": LanguageCode.UNKNOWN,
}
