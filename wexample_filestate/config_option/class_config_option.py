from typing import Any, Type

from wexample_config.config_option.abstract_config_option import AbstractConfigOption


class ClassConfigOption(AbstractConfigOption):
    @staticmethod
    def get_raw_value_allowed_type() -> Any:
        from wexample_filestate.item.file_state_item_directory_target import (
            FileStateItemDirectoryTarget,
        )
        from wexample_filestate.item.file_state_item_file_target import (
            FileStateItemFileTarget,
        )

        return Type[FileStateItemDirectoryTarget] | Type[FileStateItemFileTarget]
