from typing import List, TYPE_CHECKING, Type

from wexample_config.options_provider.abstract_options_provider import AbstractOptionsProvider
from wexample_filestate.option.remove_backup_max_file_size_option import RemoveBackupMaxFileSizeOption

if TYPE_CHECKING:
    from wexample_config.option.abstract_option import AbstractOption


class DefaultOptionsProvider(AbstractOptionsProvider):
    @classmethod
    def get_options(cls) -> List[Type["AbstractOption"]]:
        from wexample_config.option.children_option import ChildrenOption
        from wexample_filestate.option.default_content_option import DefaultContentOption
        from wexample_filestate.option.mode_option import ModeOption
        from wexample_filestate.option.mode_recursive_option import ModeRecursiveOption
        from wexample_config.option.name_option import NameOption
        from wexample_filestate.option.should_exist_option import ShouldExistOption
        from wexample_filestate.option.type_option import TypeOption

        return [
            ChildrenOption,
            DefaultContentOption,
            ModeOption,
            ModeRecursiveOption,
            NameOption,
            RemoveBackupMaxFileSizeOption,
            ShouldExistOption,
            TypeOption,
        ]
