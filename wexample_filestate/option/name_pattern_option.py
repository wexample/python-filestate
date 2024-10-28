from typing import Type
from types import UnionType

from wexample_filestate.option.abstract_item_option import AbstractItemOption


class NamePatternOption(AbstractItemOption):
    @staticmethod
    def get_value_type() -> Type | UnionType:
        return str
