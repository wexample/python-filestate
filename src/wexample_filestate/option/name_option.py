from __future__ import annotations

from typing import Any, Union

from wexample_config.config_option.abstract_config_option import AbstractConfigOption
from wexample_config.config_option.abstract_nested_config_option import AbstractNestedConfigOption
from wexample_filestate.option.mixin.option_mixin import OptionMixin
from wexample_helpers.decorator.base_class import base_class


@base_class
class NameOption(OptionMixin, AbstractNestedConfigOption):
    @staticmethod
    def get_raw_value_allowed_type() -> Any:
        from wexample_helpers.const.types import StringKeysDict
        
        return Union[str, dict, StringKeysDict]

    def set_value(self, raw_value: Any) -> None:
        from wexample_filestate.config_option.value_config_option import ValueConfigOption
        
        # Convert string form to dict form for consistency
        if isinstance(raw_value, str):
            raw_value = {
                ValueConfigOption.get_name(): raw_value
            }
        
        super().set_value(raw_value=raw_value)

    def get_allowed_options(self) -> list[type[AbstractConfigOption]]:
        from wexample_filestate.config_option.value_config_option import ValueConfigOption

        return [
            ValueConfigOption,
        ]

    def get_name_value(self) -> str | None:
        """Get the name value, supporting both legacy string and nested dict formats."""
        from wexample_filestate.config_option.value_config_option import ValueConfigOption
        
        value_option = self.get_option_value(ValueConfigOption, default=None)
        if value_option and not value_option.is_none():
            return value_option.get_str()
        
        return None
