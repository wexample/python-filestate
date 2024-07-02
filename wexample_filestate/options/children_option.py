from types import UnionType
from typing import Type

from wexample_filestate.options.abstract_option import AbstractOption


class ChildrenOption(AbstractOption):
    @staticmethod
    def get_name() -> str:
        return "children"

    @staticmethod
    def get_value_type() -> Type | UnionType:
        return list
