from typing import Union, Any

from wexample_config.config_option.abstract_config_option import AbstractConfigOption
from wexample_helpers.decorator.base_class import base_class


@base_class
class ModeConfigOption(AbstractConfigOption):
    @staticmethod
    def get_raw_value_allowed_type() -> Any:
        from wexample_filestate.const.files import FileSystemPermission

        return Union[str, int, FileSystemPermission]