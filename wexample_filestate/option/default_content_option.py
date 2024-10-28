from typing import Type
from types import UnionType

from wexample_filestate.option.abstract_item_option import AbstractItemOption


class DefaultContentOption(AbstractItemOption):
    @staticmethod
    def get_value_allowed_type() -> Type | UnionType:
        return str