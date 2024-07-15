from typing import Type
from types import UnionType

from wexample_filestate.options.abstract_option import AbstractOption


class DefaultContentOption(AbstractOption):
    @staticmethod
    def get_name() -> str:
        return "default_content"

    @staticmethod
    def get_value_type() -> Type | UnionType:
        return str
