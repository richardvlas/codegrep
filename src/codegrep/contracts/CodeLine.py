from dataclasses import dataclass, field
from typing import Optional, Set


@dataclass
class CodeLine:
    line_number: int
    content: str
    scopes: Set[int] = field(default_factory=set)
    is_of_interest: bool = False
    highlighted_content: Optional[str] = None
