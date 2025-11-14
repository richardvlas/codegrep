import argparse
import sys
import time
from pathlib import Path
from typing import Iterable, Iterator

import colorama
import pathspec

from codegrep.application import Application
from codegrep.config.config import Config

colorama.init()


def find_gitignore_path(start: Path) -> Path | None:
    current_path = start.resolve()
    print("Searching for .gitignore starting at:", current_path)

    for parent in [current_path] + list(current_path.parents):
        gitignore_file = parent / ".gitignore"
        if gitignore_file.exists():
            return gitignore_file
    return None


def walk_files(
    filenames: Iterable[str | Path], ignore_spec: pathspec.PathSpec, apply_ignore=False
) -> Iterator[Path]:
    for name in filenames:
        path = Path(name)

        if path.name.startswith(".") or (apply_ignore and ignore_spec.match_file(path)):
            continue

        if path.is_file():
            yield path

        elif path.is_dir():
            for child in walk_files(
                path.iterdir(),
                ignore_spec,
                True,
            ):
                yield child


def read_file_contents(filename: Path) -> str | None:
    try:
        return filename.read_text(encoding="utf-8")
    except UnicodeDecodeError as ude:
        print(f"Could not read file {filename} due to encoding error: {str(ude)}")
        return None


class CodeGrepCLI:

    def __init__(self) -> None:
        self._parser = argparse.ArgumentParser(
            description="codegrep: A tool to grep code with context-aware analysis.",
        )

    def run(self) -> int:
        self._attach_arguments()
        args = self._parser.parse_args()

        try:
            start = time.time()

            gitignore_path = find_gitignore_path(Path.cwd())
            print("Gitignore path found at:", gitignore_path)

            if gitignore_path is None:
                ignore_specification = pathspec.PathSpec.from_lines(
                    pathspec.patterns.GitWildMatchPattern, []
                )
            else:
                with gitignore_path.open("r") as f:
                    ignore_specification = pathspec.PathSpec.from_lines(
                        pathspec.patterns.GitWildMatchPattern, f
                    )

            for file_path in walk_files(set(args.filenames), ignore_specification):
                result = self._process_file(file_path, args)
                if result is None or result.strip() == "":
                    continue

                print()
                print(f"File name: {str(file_path)}")
                print(result)
                print()

            end = time.time()
            print(f"Total time taken: {end - start:.2f} seconds")

            number_of_files = len(
                list(walk_files(set(args.filenames), ignore_specification))
            )
            print(f"Unique filenames to process: {set(args.filenames)}")
            print(f"Number of files processed: {number_of_files}")

            return 0

        except FileNotFoundError:
            print(f"Error: File '{args.filename}' not found.", file=sys.stderr)
            return 1
        except KeyboardInterrupt:
            print("Operation cancelled by user.", file=sys.stderr)
            return 1
        except Exception as e:
            print(f"An unexpected error occurred: {e}", file=sys.stderr)
            return 1

    def _process_file(self, filename: Path, args: argparse.Namespace) -> str | None:
        code = read_file_contents(filename)
        if code is None:
            return None

        config = Config(
            filename=str(filename),
            code=code,
            colors=args.colors,
            color=args.color,
            verbose=args.verbose,
            line_numbers=args.line_numbers,
            last_line=True,
        )
        application = Application(config=config)
        try:
            result = application.run(
                search_pattern=args.search_pattern,
                ignore_case=args.ignore_case,
            )
            return result
        except Exception as e:
            print(
                f"An error occurred while processing file {filename}: {e}",
                file=sys.stderr,
            )
            return None

    def _attach_arguments(self):
        # Positional arguments
        self._parser.add_argument(
            "search_pattern",
            type=str,
            help="The pattern to search for in the code.",
        )
        self._parser.add_argument(
            "filenames",
            nargs="*",
            default=["."],
            help="Files or directories to search. (default: current directory).",
        )

        # Optional arguments
        self._parser.add_argument(
            "-i",
            "--ignore-case",
            action="store_true",
            help="Ignore case when searching for the pattern.",
        )
        self._parser.add_argument(
            "-c",
            "--colors",
            action="store_true",
            help="Enable colored output.",
        )
        self._parser.add_argument(
            "--color",
            type=str,
            default="red",
            choices=[
                "black",
                "red",
                "green",
                "yellow",
                "blue",
                "magenta",
                "cyan",
                "white",
            ],
            help="Color to use for highlighting (default: red).",
        )
        self._parser.add_argument(
            "-v",
            "--verbose",
            action="store_true",
            help="Enable verbose output.",
        )
        self._parser.add_argument(
            "-ln",
            "--line-numbers",
            action="store_true",
            help="Show line numbers in the output.",
        )
