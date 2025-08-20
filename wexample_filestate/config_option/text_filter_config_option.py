from typing import Any, Union, List

from wexample_helpers.const.types import StringKeysDict
from wexample_config.config_option.abstract_config_option import AbstractConfigOption
from wexample_config.config_value.nested_config_value import NestedConfigValue


class TextFilterConfigOption(AbstractConfigOption):
    @staticmethod
    def get_raw_value_allowed_type() -> Any:
        return Union[List[str], StringKeysDict]

    def get_value_class_type(self) -> type[NestedConfigValue]:
        # Use NestedConfigValue to ease nested access like search('trim.char')
        return NestedConfigValue

    def get_trimmed_char(self) -> str:
        # Default behavior remains trimming newlines
        default_char = "\n"

        value = self.get_value()
        if value is None:
            return default_char

        # If configured as a dict, allow specifying trim.char
        if value.is_dict():
            found = value.search("trim.char")
            if found is not None and found.is_str():
                return found.get_str()

        # Fallback (e.g., list form ["trim"]) uses default newline
        return default_char