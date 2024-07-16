from typing import Type, Union
from types import UnionType

from wexample_filestate.options.abstract_option import AbstractOption
from wexample_filestate.options_values.string_option_value import StringOptionValue


class ContentOption(AbstractOption):
    @staticmethod
    def get_name() -> str:
        return "content"

    @staticmethod
    def get_value_type() -> Type | UnionType:
        return Union[str | StringOptionValue]
