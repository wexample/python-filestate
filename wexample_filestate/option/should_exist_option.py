from typing import Type
from types import UnionType

from wexample_config.option.abstract_option import AbstractOption


class ShouldExistOption(AbstractOption):
    @staticmethod
    def get_value_class_type() -> Type | UnionType:
        return bool
