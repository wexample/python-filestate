from typing import Type
from types import UnionType
from wexample_filestate.const.files import FileSystemPermission
from wexample_filestate.option.abstract_item_option import AbstractItemOption


class ModeRecursiveOption(AbstractItemOption):
    value: FileSystemPermission

    @staticmethod
    def get_value_allowed_type() -> Type | UnionType:
        return bool
