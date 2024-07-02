from typing import Type
from types import UnionType

from wexample_filestate.const.enums import DiskItemType
from wexample_filestate.options.abstract_option import AbstractOption


class TypeOption(AbstractOption):
    @staticmethod
    def get_name() -> str:
        return "type"

    @staticmethod
    def get_value_type() -> Type | UnionType:
        return DiskItemType
