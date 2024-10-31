from typing import Any

from wexample_config.config_option.abstract_config_option import AbstractConfigOption
from wexample_filestate.const.files import FileSystemPermission


class ModeRecursiveConfigOption(AbstractConfigOption):
    value: FileSystemPermission

    @staticmethod
    def get_raw_value_allowed_type() -> Any:
        return bool
