from typing import Type
from types import UnionType
from wexample_filestate.const.files import FileSystemPermission
from wexample_config.option.abstract_option import AbstractOption


class ModeRecursiveOption(AbstractOption):
    value: FileSystemPermission

    @staticmethod
    def get_value_type() -> Type | UnionType:
        return bool
