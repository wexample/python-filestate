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
class ContentOption(OptionMixin, AbstractNestedConfigOption):
    @staticmethod
    def get_raw_value_allowed_type() -> Any:
        from wexample_filestate.config_value.content_config_value import ContentConfigValue
        from wexample_helpers.const.types import StringKeysDict

        return Union[str, dict, StringKeysDict, ContentConfigValue]

    def set_value(self, raw_value: Any) -> None:
        from wexample_filestate.option.content.value_option import ValueOption
        
        # Convert string form to dict form for consistency
        if isinstance(raw_value, str):
            raw_value = {
                ValueOption.get_name(): raw_value
            }
        
        super().set_value(raw_value=raw_value)

    def get_allowed_options(self) -> list[type[AbstractConfigOption]]:
        from wexample_filestate.option.content.value_option import ValueOption
        from wexample_filestate.option.content.sort_lines_option import SortLinesOption
        from wexample_filestate.option.content.unique_lines_option import UniqueLinesOption

        return [
            ValueOption,
            SortLinesOption,
            UniqueLinesOption,
        ]

    def create_required_operation(self, target: TargetFileOrDirectoryType) -> AbstractOperation | None:
        """Create operation using child options."""
        return self._create_child_required_operation(target=target)
