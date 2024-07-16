from typing import List, TYPE_CHECKING, Type

from wexample_filestate.operation.file_write_operation import FileWriteOperation
from wexample_filestate.options.class_option import ClassOption
from wexample_filestate.options.children_option import ChildrenOption
from wexample_filestate.options.content_option import ContentOption
from wexample_filestate.options.default_content_option import DefaultContentOption
from wexample_filestate.options.name_pattern_option import NamePatternOption
from wexample_filestate.options.remove_backup_max_file_size_option import RemoveBackupMaxFileSizeOption
from wexample_filestate.options.type_option import TypeOption
from wexample_filestate.options_provider.abstract_options_provider import AbstractOptionsProvider

if TYPE_CHECKING:
    from wexample_filestate.options.abstract_option import AbstractOption
    from wexample_filestate.operation.abstract_operation import AbstractOperation


class DefaultOptionsProvider(AbstractOptionsProvider):
    def get_options(self) -> List[Type["AbstractOption"]]:
        from wexample_filestate.options.name_option import NameOption
        from wexample_filestate.options.mode_option import ModeOption
        from wexample_filestate.options.mode_recursive_option import ModeRecursiveOption
        from wexample_filestate.options.should_exist_option import ShouldExistOption

        return [
            ChildrenOption,
            ClassOption,
            ContentOption,
            DefaultContentOption,
            ModeOption,
            ModeRecursiveOption,
            NameOption,
            NamePatternOption,
            RemoveBackupMaxFileSizeOption,
            ShouldExistOption,
            TypeOption
        ]

    def get_operations(self) -> List[Type["AbstractOperation"]]:
        from wexample_filestate.operation.item_change_mode_operation import ItemChangeModeOperation
        from wexample_filestate.operation.file_create_operation import FileCreateOperation
        from wexample_filestate.operation.file_remove_operation import FileRemoveOperation

        return [
            FileCreateOperation,
            FileRemoveOperation,
            FileWriteOperation,
            ItemChangeModeOperation,
        ]
