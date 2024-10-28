from types import UnionType
from typing import Type

from wexample_filestate.option.abstract_item_option import AbstractItemOption


class ClassOption(AbstractItemOption):
    @staticmethod
    def get_value_allowed_type() -> Type | UnionType:
        from wexample_filestate.item.file_state_item_file_target import FileStateItemFileTarget
        from wexample_filestate.item.file_state_item_directory_target import FileStateItemDirectoryTarget

        return FileStateItemDirectoryTarget | FileStateItemFileTarget
