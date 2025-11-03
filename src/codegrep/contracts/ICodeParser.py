from abc import ABC, abstractmethod

from tree_sitter import Tree


class ICodeParser(ABC):
    """Interface for parsing code into an abstract syntax tree (AST)."""

    @abstractmethod
    def parse(self, code: str, language: str) -> Tree:
        pass
