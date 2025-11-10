from enum import Enum


class AnsiForeground(Enum):
    """ANSI text (foreground) colors."""

    RESET = "\033[39m"

    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[97m"

    @classmethod
    def from_name(cls, name: str) -> "AnsiForeground":
        try:
            return cls[name.upper()]
        except KeyError:
            raise ValueError(f"No foreground color named '{name}'")


class AnsiBackground(Enum):
    """ANSI background colors."""

    RESET = "\033[49m"

    BLACK = "\033[40m"
    RED = "\033[41m"
    GREEN = "\033[42m"
    YELLOW = "\033[43m"
    BLUE = "\033[44m"
    MAGENTA = "\033[45m"
    CYAN = "\033[46m"
    WHITE = "\033[47m"

    @classmethod
    def from_name(cls, name: str) -> "AnsiBackground":
        try:
            return cls[name.upper()]
        except KeyError:
            raise ValueError(f"No background color named '{name}'")
