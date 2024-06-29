from typing import List, TYPE_CHECKING, Type

from wexample_filestate.options.children_option import ChildrenOption
from wexample_filestate.options.name_pattern_option import NamePatternOption
from wexample_filestate.options.remove_backup_max_file_size_option import RemoveBackupMaxFileSizeOption
from wexample_filestate.options.type_option import TypeOption
from wexample_filestate.options_provider.abstract_options_provider import AbstractOptionsProvider

if TYPE_CHECKING:
    from wexample_filestate.options.abstract_option import AbstractOption


class DefaultOptionsProvider(AbstractOptionsProvider):
    def get_options(self) -> List[Type["AbstractOption"]]:
        from wexample_filestate.options.name_option import NameOption
        from wexample_filestate.options.mode_option import ModeOption
        from wexample_filestate.options.should_exist_option import ShouldExistOption

        return [
            ChildrenOption,
            ModeOption,
            NameOption,
            NamePatternOption,
            RemoveBackupMaxFileSizeOption,
            ShouldExistOption,
            TypeOption
        ]
