from __future__ import annotations

from typing import TYPE_CHECKING, Any, Union

from wexample_config.config_option.abstract_config_option import AbstractConfigOption
from wexample_config.config_option.abstract_nested_config_option import AbstractNestedConfigOption
from wexample_filestate.option.mixin.option_mixin import OptionMixin
from wexample_helpers.decorator.base_class import base_class

if TYPE_CHECKING:
    from wexample_filestate.operation.abstract_operation import AbstractOperation
    from wexample_filestate.const.types_state_items import TargetFileOrDirectoryType


@base_class
class OnBadFormatOption(OptionMixin, AbstractNestedConfigOption):
    @staticmethod
    def get_raw_value_allowed_type() -> Any:
        from wexample_filestate.config_value.on_bad_format_config_value import OnBadFormatConfigValue
        
        return Union[str, dict, OnBadFormatConfigValue]

    def set_value(self, raw_value: Any) -> None:
        from wexample_filestate.config_option.action_config_option import ActionConfigOption
        
        # Convert string form to dict form for consistency
        if isinstance(raw_value, str):
            raw_value = {
                ActionConfigOption.get_name(): raw_value
            }
        
        super().set_value(raw_value=raw_value)

    def get_allowed_options(self) -> list[type[AbstractConfigOption]]:
        from wexample_filestate.config_option.action_config_option import ActionConfigOption

        return [
            ActionConfigOption,
        ]

    def create_required_operation(self, target: TargetFileOrDirectoryType) -> AbstractOperation | None:
        """Create operation based on name format validation and enforcement action."""
        from wexample_filestate.option.name_format_option import NameFormatOption
        from wexample_filestate.config_option.action_config_option import ActionConfigOption
        from wexample_filestate.operation.file_remove_operation import FileRemoveOperation
        from wexample_filestate.operation.file_rename_operation import FileRenameOperation

        name_format_option = target.get_option(NameFormatOption)
        
        # Get the current name
        current_name = target.get_item_name()
        if not current_name:
            return None
        
        # Validate the name format
        if name_format_option.validate_name(current_name):
            return None  # Name is valid, no action needed
        
        # Get the enforcement action
        action_option = self.get_option_value(ActionConfigOption, default=None)
        if not action_option or action_option.is_none():
            return None
        
        action = action_option.get_str()
        
        if action == "delete":
            return FileRemoveOperation(
                option=self, 
                target=target,
                description=f"Delete file '{target.get_item_name()}' due to bad format"
            )
        elif action == "rename":
            current_name = target.get_item_name()
            new_name = self._generate_compliant_name(current_name, name_format_option)

            if new_name and new_name != current_name:
                return FileRenameOperation(
                    option=self,
                    target=target,
                    new_name=new_name,
                    description=f"Rename file from '{current_name}' to '{new_name}' to fix format"
                )

            return self._create_rename_operation(target, name_format_option)
        elif action == "error":
            raise ValueError(f"Name format validation failed for: {current_name}")

        return None

    def _create_rename_operation(self, target: TargetFileOrDirectoryType, name_format_option):
        """Create operation to rename the file/directory to match format."""

        
        return None

    def _generate_compliant_name(self, current_name: str, name_format_option) -> str | None:
        """Generate a compliant name based on format rules."""
        from wexample_filestate.config_option.case_format_config_option import CaseFormatConfigOption
        from wexample_filestate.config_option.prefix_config_option import PrefixConfigOption
        from wexample_filestate.config_option.suffix_config_option import SuffixConfigOption
        
        new_name = current_name
        
        # Apply case format
        case_format_option = name_format_option.get_option_value(CaseFormatConfigOption, default=None)
        if case_format_option and not case_format_option.is_none():
            case_format = case_format_option.get_str()
            new_name = self._apply_case_format(new_name, case_format)
        
        # Apply prefix
        prefix_option = name_format_option.get_option_value(PrefixConfigOption, default=None)
        if prefix_option and not prefix_option.is_none():
            prefix = prefix_option.get_str()
            if not new_name.startswith(prefix):
                new_name = prefix + new_name
        
        # Apply suffix
        suffix_option = name_format_option.get_option_value(SuffixConfigOption, default=None)
        if suffix_option and not suffix_option.is_none():
            suffix = suffix_option.get_str()
            if not new_name.endswith(suffix):
                new_name = new_name + suffix
        
        return new_name

    def _apply_case_format(self, name: str, case_format: str) -> str:
        """Apply case format transformation to name."""
        if case_format == "uppercase":
            return name.upper()
        elif case_format == "lowercase":
            return name.lower()
        elif case_format == "camelCase":
            return self._to_camel_case(name)
        elif case_format == "snake_case":
            return self._to_snake_case(name)
        elif case_format == "kebab-case":
            return self._to_kebab_case(name)
        return name

    def _to_camel_case(self, name: str) -> str:
        """Convert name to camelCase."""
        import re
        # Split on non-alphanumeric characters and capitalize each word except first
        words = re.split(r'[^a-zA-Z0-9]', name.lower())
        return words[0] + ''.join(word.capitalize() for word in words[1:] if word)

    def _to_snake_case(self, name: str) -> str:
        """Convert name to snake_case."""
        import re
        # Replace non-alphanumeric with underscore and convert to lowercase
        return re.sub(r'[^a-zA-Z0-9]', '_', name.lower())

    def _to_kebab_case(self, name: str) -> str:
        """Convert name to kebab-case."""
        import re
        # Replace non-alphanumeric with hyphen and convert to lowercase
        return re.sub(r'[^a-zA-Z0-9]', '-', name.lower())
