from contracts.ICodeParser import ICodeParser
from tree_sitter import Parser, Tree
from tree_sitter_language_pack import get_parser


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


if __name__ == "__main__":
    code = """
class MachineConnector(ABC):
    # Abstract base class for machine connectors.
    
    @abstractmethod
    def connect(self) -> None:
        pass
    
    @abstractmethod
    def disconnect(self) -> None:
        pass
"""

    parser = TreeSitterCodeParser()
    tree = parser.parse(code, "python")
    print(f"Parsed tree: {tree}")
    print(f"Root node: {tree.root_node}")
    print(f"Root node children: {tree.root_node.children}")
