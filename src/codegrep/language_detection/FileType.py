from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class FileType:
    name: str

    @classmethod
    def from_filename(cls, filename: str) -> "FileType":
        file_path = Path(filename)
        return cls(name=file_path.suffix.lower() or file_path.name)
