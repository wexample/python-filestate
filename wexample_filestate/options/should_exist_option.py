from typing import Type
from types import UnionType

from wexample_filestate.options.abstract_option import AbstractOption


class ShouldExistOption(AbstractOption):
    @staticmethod
    def get_name() -> str:
        return "should_exist"

    @staticmethod
    def get_value_type() -> Type | UnionType:
        return bool
