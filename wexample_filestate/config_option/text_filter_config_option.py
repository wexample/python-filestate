from typing import Any, Union, List

from wexample_helpers.const.types import StringKeysDict
from wexample_config.config_option.abstract_config_option import AbstractConfigOption


class TextFilterConfigOption(AbstractConfigOption):
    @staticmethod
    def get_raw_value_allowed_type() -> Any:
        return Union[List[str], StringKeysDict]

    def get_trimmed_char(self) -> str:
        return "\n"