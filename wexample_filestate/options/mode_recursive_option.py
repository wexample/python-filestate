from typing import Type
from types import UnionType
from wexample_filestate.const.types import FileSystemPermission
from wexample_filestate.options.abstract_option import AbstractOption


class ModeRecursiveOption(AbstractOption):
    value: FileSystemPermission

    @staticmethod
    def get_name() -> str:
        return "mode_recursive"

    @staticmethod
    def get_value_type() -> Type | UnionType:
        return bool
