from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any, Union, Callable

from wexample_config.config_option.abstract_config_option import AbstractConfigOption
from wexample_config.config_option.abstract_nested_config_option import AbstractNestedConfigOption
from wexample_filestate.option.mixin.option_mixin import OptionMixin
from wexample_helpers.decorator.base_class import base_class

if TYPE_CHECKING:
    from wexample_filestate.operation.abstract_operation import AbstractOperation
    from wexample_filestate.const.types_state_items import TargetFileOrDirectoryType


@base_class
class NameOption(OptionMixin, AbstractNestedConfigOption):
    @staticmethod
    def get_raw_value_allowed_type() -> Any:
        from wexample_filestate.config_value.name_config_value import NameConfigValue
        
        return Union[str, Path, dict, NameConfigValue, Callable]

    def set_value(self, raw_value: Any) -> None:
        from wexample_filestate.option.name.value_option import ValueOption

        if isinstance(raw_value, Path):
            raw_value = str(raw_value)

        # Store callable directly without conversion
        if callable(raw_value):
            self._callable_value = raw_value
            # Create a placeholder dict to satisfy the nested config structure
            raw_value = {
                ValueOption.get_name(): None
            }
        # Convert string form to dict form for consistency
        elif isinstance(raw_value, str):
            raw_value = {
                ValueOption.get_name(): raw_value
            }

        super().set_value(raw_value=raw_value)

    def get_allowed_options(self) -> list[type[AbstractConfigOption]]:
        from wexample_filestate.option.name.value_option import ValueOption
        from wexample_filestate.option.name.case_format_option import CaseFormatOption
        from wexample_filestate.option.name.regex_option import RegexOption
        from wexample_filestate.option.name.prefix_option import PrefixOption
        from wexample_filestate.option.name.suffix_option import SuffixOption
        from wexample_filestate.option.name.on_bad_format_option import OnBadFormatOption

        return [
            ValueOption,
            CaseFormatOption,
            RegexOption,
            PrefixOption,
            SuffixOption,
            OnBadFormatOption,
        ]

    def get_name_value(self) -> str | None:
        """Get the name value, supporting both legacy string, nested dict, and callable formats."""
        from wexample_filestate.option.name.value_option import ValueOption
        
        # Check if we have a callable value stored
        if hasattr(self, '_callable_value') and callable(self._callable_value):
            try:
                # Execute the callable with self as parameter
                result = self._callable_value(self)
                return str(result) if result is not None else None
            except Exception:
                # If callable fails, fall back to None
                return None
        
        value_option = self.get_option_value(ValueOption, default=None)
        if value_option and not value_option.is_none():
            return value_option.get_str()
        
        return None

    def create_required_operation(self, target: TargetFileOrDirectoryType) -> AbstractOperation | None:
        """Create operation via OnBadFormatOption if name format validation fails."""
        from wexample_filestate.option.name.on_bad_format_option import OnBadFormatOption

        # Check if OnBadFormatOption is configured
        on_bad_format_option = self.get_option(OnBadFormatOption)
        if on_bad_format_option:
            return on_bad_format_option.create_required_operation(target)
        
        return None

    def validate_name(self, name: str) -> bool:
        """Validate if a name matches all format rules using child options."""
        from wexample_filestate.option.name.case_format_option import CaseFormatOption
        from wexample_filestate.option.name.regex_option import RegexOption
        from wexample_filestate.option.name.prefix_option import PrefixOption
        from wexample_filestate.option.name.suffix_option import SuffixOption
        
        # Check each format rule using child options
        for option_class in [CaseFormatOption, RegexOption, PrefixOption, SuffixOption]:
            option = self.get_option(option_class)
            if option and not option.validate_name(name):
                return False
        
        return True
