from typing import Type, Union
from types import UnionType

from wexample_filestate.option.abstract_item_config_option import AbstractItemConfigOption


class ContentConfigOption(AbstractItemConfigOption):
    @staticmethod
    def get_value_allowed_type() -> Type | UnionType:
        return Union[str]
