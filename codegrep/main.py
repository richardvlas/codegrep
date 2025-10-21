import argparse
import os
import sys
from pathlib import Path
from typing import Iterable

import pathspec


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Grep code snippets in files.")

    # Positional args
    parser.add_argument("pattern", nargs="?", help="pattern to search for in the code")
    parser.add_argument("filenames", nargs="*", default=".", help="files to search in")

    # Optional args
    parser.add_argument(
        "-e", "--encoding", default="utf-8", help="specify file encoding"
    )
    parser.add_argument(
        "--languages", action="store_true", help="show supported languages and exit"
    )
    parser.add_argument(
        "--color", dest="color", action="store_true", help="force color output"
    )
    parser.add_argument(
        "--no-color", dest="color", action="store_false", help="disable color output"
    )
    parser.add_argument(
        "--no-gitignore", action="store_true", help="ignore .gitignore files"
    )

    return parser


def find_nearest_gitignore_path(search_path: Path | None = None) -> Path | None:
    """
    Find the nearest .gitignore file starting from the given search path.
    If no path is provided, start from the current working directory.

    :param search_path: Path to start searching from.
    :return: Path to the nearest .gitignore file or None if not found.
    """
    if search_path is None:
        search_path = Path.cwd()

    absolute_search_paths = (search_path.resolve(),) + tuple(
        search_path.resolve().parents
    )

    for current_directory in absolute_search_paths:
        gitignore_path = current_directory / ".gitignore"
        if gitignore_path.exists():
            return gitignore_path.resolve()
    return None


def enumerate_files(
    filenames: Iterable[Path | str],
    path_spec: pathspec.PathSpec | None,
    apply_spec: bool,
) -> Iterable[Path]:
    for filename in filenames:
        filename = Path(filename)

        # Path(".").name == "" on some platforms, se we will recurse it
        if (
            filename.name.startswith(".")
            or apply_spec
            and path_spec.match_file(filename)
        ):
            continue

        if filename.is_file():
            yield filename

        elif filename.is_dir():
            for sub_file_name in enumerate_files(filename.iterdir(), path_spec, True):
                yield sub_file_name


def process_filename(filename: Path, args: argparse.Namespace) -> None:
    try:
        code = filename.read_text(encoding=args.encoding)
        print(f"Processing {filename}...")
        print(f"Content:\n{code[:200]}...")  # Print first 100 characters
    except UnicodeDecodeError:
        print(f"Error reading {filename}: Unsupported encoding {args.encoding}")
        return


def main():
    parser = build_parser()
    args = parser.parse_args()

    # if stdout is not a terminal, disable color output
    if args.color is None:
        args.color = os.isatty(1)

    # TODO: To be deleted
    print(f"Pattern to search for: {args.pattern}")
    print(f"Files to search in: {args.filenames}")
    print(f"File encoding: {args.encoding}")
    print(f"Color output enabled: {args.color}")
    print(f"No gitignore: {args.no_gitignore}")

    # If languages flag is set, show supported languages and exit
    if args.languages:
        print("Supported languages: TBD")
        return None
    elif args.pattern is None:
        print("No pattern provided. Please provide a pattern to search for.")
        return 1

    if args.no_gitignore is True:
        gitignore_path = None
    else:
        gitignore_path = find_nearest_gitignore_path()

    if gitignore_path:
        with gitignore_path.open() as gitignore_file:
            path_spec = pathspec.PathSpec.from_lines("gitwildmatch", gitignore_file)
    else:
        path_spec = pathspec.PathSpec.from_lines("gitwildmatch", [])

    for file_name in enumerate_files(args.filenames, path_spec, False):
        print(f"File found: {file_name}")
        process_filename(file_name, args)


if __name__ == "__main__":
    result = main()
    sys.exit(result)
