from typing import Any

from wexample_config.config_option.abstract_config_option import AbstractConfigOption


class ClassConfigOption(AbstractConfigOption):
    @staticmethod
    def get_value_allowed_type() -> Any:
        from wexample_filestate.item.file_state_item_file_target import FileStateItemFileTarget
        from wexample_filestate.item.file_state_item_directory_target import FileStateItemDirectoryTarget

        return FileStateItemDirectoryTarget | FileStateItemFileTarget
