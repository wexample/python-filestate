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
        from wexample_filestate.config_option.case_format_config_option import CaseFormatConfigOption
        
        # Convert string form to dict form for consistency
        if isinstance(raw_value, str):
            raw_value = {
                CaseFormatConfigOption.get_name(): raw_value
            }
        
        super().set_value(raw_value=raw_value)

    def get_allowed_options(self) -> list[type[AbstractConfigOption]]:
        from wexample_filestate.config_option.case_format_config_option import CaseFormatConfigOption
        from wexample_filestate.config_option.regex_config_option import RegexConfigOption
        from wexample_filestate.config_option.prefix_config_option import PrefixConfigOption
        from wexample_filestate.config_option.suffix_config_option import SuffixConfigOption

        return [
            CaseFormatConfigOption,
            RegexConfigOption,
            PrefixConfigOption,
            SuffixConfigOption,
        ]

    def create_required_operation(self, target: TargetFileOrDirectoryType) -> AbstractOperation | None:
        """Create operation if name format validation fails."""
        # This option doesn't create operations directly
        # It's used by OnBadFormatOption to validate names
        return None

    def validate_name(self, name: str) -> bool:
        """Validate if a name matches the format rules."""
        from wexample_filestate.config_option.case_format_config_option import CaseFormatConfigOption
        from wexample_filestate.config_option.regex_config_option import RegexConfigOption
        from wexample_filestate.config_option.prefix_config_option import PrefixConfigOption
        from wexample_filestate.config_option.suffix_config_option import SuffixConfigOption
        
        # Check case format
        case_format_option = self.get_option_value(CaseFormatConfigOption, default=None)
        if case_format_option and not case_format_option.is_none():
            case_format = case_format_option.get_str()
            if not self._validate_case_format(name, case_format):
                return False
        
        # Check regex
        regex_option = self.get_option_value(RegexConfigOption, default=None)
        if regex_option and not regex_option.is_none():
            regex_pattern = regex_option.get_str()
            if not re.match(regex_pattern, name):
                return False
        
        # Check prefix
        prefix_option = self.get_option_value(PrefixConfigOption, default=None)
        if prefix_option and not prefix_option.is_none():
            prefix = prefix_option.get_str()
            if not name.startswith(prefix):
                return False
        
        # Check suffix
        suffix_option = self.get_option_value(SuffixConfigOption, default=None)
        if suffix_option and not suffix_option.is_none():
            suffix = suffix_option.get_str()
            if not name.endswith(suffix):
                return False
        
        return True

    def _validate_case_format(self, name: str, case_format: str) -> bool:
        """Validate case format of the name."""
        if case_format == "uppercase":
            return name.isupper()
        elif case_format == "lowercase":
            return name.islower()
        elif case_format == "camelCase":
            return self._is_camel_case(name)
        elif case_format == "snake_case":
            return self._is_snake_case(name)
        elif case_format == "kebab-case":
            return self._is_kebab_case(name)
        return True

    def _is_camel_case(self, name: str) -> bool:
        """Check if name is in camelCase format."""
        return re.match(r'^[a-z][a-zA-Z0-9]*$', name) is not None

    def _is_snake_case(self, name: str) -> bool:
        """Check if name is in snake_case format."""
        return re.match(r'^[a-z0-9]+(_[a-z0-9]+)*$', name) is not None

    def _is_kebab_case(self, name: str) -> bool:
        """Check if name is in kebab-case format."""
        return re.match(r'^[a-z0-9]+(-[a-z0-9]+)*$', name) is not None
