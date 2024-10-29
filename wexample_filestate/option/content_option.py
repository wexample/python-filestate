from typing import Type, Union
from types import UnionType

from wexample_filestate.option.abstract_item_option import AbstractItemOption


class ContentOption(AbstractItemOption):
    @staticmethod
    def get_value_allowed_type() -> Type | UnionType:
        return Union[str]
