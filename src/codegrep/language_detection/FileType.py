from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class FileType:
    name: str

    @classmethod
    def from_filename(cls, filename: str) -> "FileType":
        file_path = Path(filename)
        return cls(name=file_path.suffix.lower() or file_path.name)


if __name__ == "__main__":
    ft1 = FileType.from_filename("example.py")
    print(ft1)  # Output: FileType(name='.py')

    ft2 = FileType.from_filename("Dockerfile")
    print(ft2)  # Output: FileType(name='Dockerfile')

    ft3 = FileType.from_filename("archive")
    print(ft3)  # Output: FileType(name='archive')

    ft4 = FileType.from_filename("D://path/to/file.TS")
    print(ft4)  # Output: FileType(name='.ts')

    ft5 = FileType.from_filename("/usr/.dockerfile")
    print(ft5)  # Output: FileType(name='.dockerfile')

    # Demonstrating it for all possible go langauge extensions
    go_extensions = [".go", ".mod", ".sum"]
    for ext in go_extensions:
        ft = FileType.from_filename(f"project{ext}")
        print(ft)  # Output: FileType(name='.go'), etc.
