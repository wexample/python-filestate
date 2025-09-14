from __future__ import annotations

from typing import TYPE_CHECKING, Any, ClassVar, Union

from wexample_config.config_option.abstract_config_option import AbstractConfigOption

if TYPE_CHECKING:
    from wexample_config.config_value.nested_config_value import NestedConfigValue

from wexample_filestate.option.mixin.option_mixin import OptionMixin
from wexample_helpers.decorator.base_class import base_class


@base_class
class TextFilterOption(OptionMixin, AbstractConfigOption):
    OPTION_NAME_TRIM: ClassVar[str] = "trim"
    OPTION_NAME_ENSURE_NEWLINE: ClassVar[str] = "ensure_newline"

    @staticmethod
    def get_raw_value_allowed_type() -> Any:
        from wexample_helpers.const.types import StringKeysDict

        return Union[list[str], StringKeysDict]

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

    def get_value_class_type(self) -> type[NestedConfigValue]:
        from wexample_config.config_value.nested_config_value import NestedConfigValue

        # Use NestedConfigValue to ease nested access like search('trim.char')
        return NestedConfigValue
