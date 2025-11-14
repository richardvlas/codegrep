from tree_sitter import Parser, Tree
from tree_sitter_language_pack import get_parser

from codegrep.contracts.ICodeParser import ICodeParser


class TreeSitterCodeParser(ICodeParser):

    def parse(self, code: str, language: str) -> Tree:
        parser: Parser = self._resolve_code_parser(language=language)
        tree: Tree = parser.parse(bytes(code, encoding="utf8"))
        return tree

    def _resolve_code_parser(self, language: str) -> Parser:
        try:
            parser: Parser = get_parser(language_name=language)
            return parser
        except LookupError as lue:
            raise ValueError(
                f"There is no parser for {language} language. (errorMessage={str(lue)})"
            ) from lue
