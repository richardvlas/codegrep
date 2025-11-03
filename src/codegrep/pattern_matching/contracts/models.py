from dataclasses import dataclass


@dataclass(frozen=True)
class MatchSpan:
    start: int
    end: int


@dataclass(frozen=True)
class LineMatch:
    line_number: int
    spans: list[MatchSpan]


@dataclass(frozen=True)
class PatternMatchResult:
    pattern: str
    matches: list[LineMatch]
