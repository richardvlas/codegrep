from contracts.ICodeParser import ICodeParser
from tree_sitter import Parser, Tree
from tree_sitter_language_pack import get_parser


class TreeSitterCodeParser(ICodeParser):

    def parse(self, code: str, langauge: str) -> Tree:
        parser = self._resolve_code_parser(langauge)
        tree = parser.parse(bytes(code, "utf8"))
        return tree

    def _resolve_code_parser(self, language: str) -> Parser:
        try:
            parser = get_parser(language)
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
    print(tree)
    print(tree.root_node)
    print(tree.root_node.children)
