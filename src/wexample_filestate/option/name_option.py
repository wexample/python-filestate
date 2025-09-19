from __future__ import annotations

from typing import Any, Union, Callable

from wexample_config.config_option.abstract_config_option import AbstractConfigOption
from wexample_config.config_option.abstract_nested_config_option import AbstractNestedConfigOption
from wexample_filestate.option.mixin.option_mixin import OptionMixin
from wexample_helpers.decorator.base_class import base_class


@base_class
class NameOption(OptionMixin, AbstractNestedConfigOption):
    @staticmethod
    def get_raw_value_allowed_type() -> Any:
        from wexample_filestate.config_value.name_config_value import NameConfigValue
        
        return Union[str, dict, NameConfigValue, Callable]

    def prepare_value(self, raw_value: Any) -> None:
        from wexample_filestate.config_option.value_config_option import ValueConfigOption
        
        # Store callable directly without conversion
        if callable(raw_value):
            self._callable_value = raw_value
            # Create a placeholder dict to satisfy the nested config structure
            raw_value = {
                ValueConfigOption.get_name(): None
            }
        # Convert string form to dict form for consistency
        elif isinstance(raw_value, str):
            raw_value = {
                ValueConfigOption.get_name(): raw_value
            }
        
        super().prepare_value(raw_value=raw_value)

    def get_allowed_options(self) -> list[type[AbstractConfigOption]]:
        from wexample_filestate.config_option.value_config_option import ValueConfigOption

        return [
            ValueConfigOption,
        ]

    def get_name_value(self) -> str | None:
        """Get the name value, supporting both legacy string, nested dict, and callable formats."""
        from wexample_filestate.config_option.value_config_option import ValueConfigOption
        
        # Check if we have a callable value stored
        if hasattr(self, '_callable_value') and callable(self._callable_value):
            try:
                # Execute the callable with self as parameter
                result = self._callable_value(self)
                return str(result) if result is not None else None
            except Exception:
                # If callable fails, fall back to None
                return None
        
        value_option = self.get_option_value(ValueConfigOption, default=None)
        if value_option and not value_option.is_none():
            return value_option.get_str()
        
        return None
