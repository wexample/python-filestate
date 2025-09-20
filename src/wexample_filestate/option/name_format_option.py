from __future__ import annotations

from typing import TYPE_CHECKING, Any, Union
import re

from wexample_config.config_option.abstract_config_option import AbstractConfigOption
from wexample_config.config_option.abstract_nested_config_option import AbstractNestedConfigOption
from wexample_filestate.option.mixin.option_mixin import OptionMixin
from wexample_helpers.decorator.base_class import base_class

if TYPE_CHECKING:
    from wexample_filestate.operation.abstract_operation import AbstractOperation
    from wexample_filestate.const.types_state_items import TargetFileOrDirectoryType


@base_class
class NameFormatOption(OptionMixin, AbstractNestedConfigOption):
    @staticmethod
    def get_raw_value_allowed_type() -> Any:
        from wexample_filestate.config_value.name_format_config_value import NameFormatConfigValue
        
        return Union[str, dict, NameFormatConfigValue]

    def set_value(self, raw_value: Any) -> None:
        from wexample_filestate.option.name_format.case_format_option import CaseFormatOption
        
        # Convert string form to dict form for consistency
        if isinstance(raw_value, str):
            raw_value = {
                CaseFormatOption.get_name(): raw_value
            }
        
        super().set_value(raw_value=raw_value)

    def get_allowed_options(self) -> list[type[AbstractConfigOption]]:
        from wexample_filestate.option.name_format.case_format_option import CaseFormatOption
        from wexample_filestate.option.name_format.regex_option import RegexOption
        from wexample_filestate.option.name_format.prefix_option import PrefixOption
        from wexample_filestate.option.name_format.suffix_option import SuffixOption
        from wexample_filestate.option.name_format.on_bad_format_option import OnBadFormatOption

        return [
            CaseFormatOption,
            RegexOption,
            PrefixOption,
            SuffixOption,
            OnBadFormatOption,
        ]

    def create_required_operation(self, target: TargetFileOrDirectoryType) -> AbstractOperation | None:
        """Create operation via OnBadFormatOption if name format validation fails."""
        from wexample_filestate.option.name_format.on_bad_format_option import OnBadFormatOption
        
        # Check if OnBadFormatOption is configured
        on_bad_format_option = self.get_option(OnBadFormatOption)
        if on_bad_format_option:
            return on_bad_format_option.create_required_operation(target, parent_option=self)
        
        return None

    def validate_name(self, name: str) -> bool:
        """Validate if a name matches all format rules using child options."""
        from wexample_filestate.option.name_format.case_format_option import CaseFormatOption
        from wexample_filestate.option.name_format.regex_option import RegexOption
        from wexample_filestate.option.name_format.prefix_option import PrefixOption
        from wexample_filestate.option.name_format.suffix_option import SuffixOption
        
        # Check each format rule using child options
        for option_class in [CaseFormatOption, RegexOption, PrefixOption, SuffixOption]:
            option = self.get_option(option_class)
            if option and not option.validate_name(name):
                return False
        
        return True
