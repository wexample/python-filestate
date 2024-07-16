from types import UnionType
from typing import Type

from wexample_filestate.options.abstract_option import AbstractOption


class ClassOption(AbstractOption):
    @staticmethod
    def get_name() -> str:
        return "class"

    @staticmethod
    def get_value_type() -> Type | UnionType:
        from wexample_filestate.item.file_state_item_file_target import FileStateItemFileTarget
        from wexample_filestate.item.file_state_item_directory_target import FileStateItemDirectoryTarget

        return FileStateItemDirectoryTarget | FileStateItemFileTarget
