from __future__ import annotations

from typing import TYPE_CHECKING, Any

from wexample_config.config_option.abstract_config_option import AbstractConfigOption
from wexample_filestate.option.mixin.option_mixin import OptionMixin

if TYPE_CHECKING:
    from wexample_filestate.const.types_state_items import TargetFileOrDirectoryType


class AbstractContentChildOption(OptionMixin, AbstractConfigOption):
    @staticmethod
    def get_raw_value_allowed_type() -> Any:
        return bool
    
    def _read_current_content(self, target: TargetFileOrDirectoryType) -> str | None:
        """Read current file content, return None if file doesn't exist."""
        if not target.source or not target.source.get_path().exists():
            return None
        return target.get_local_file().read()

    def _get_base_content(self, target: TargetFileOrDirectoryType) -> str | None:
        """Get the base content from the parent ContentOption."""
        from wexample_filestate.option.content.value_option import ValueOption
        
        parent = self.get_parent()
        if not parent:
            return None
            
        value_option = parent.get_option_value(ValueOption, default=None)
        if not value_option or value_option.is_none():
            return None
            
        target_content = value_option.get_str()
        if target_content is None:
            return None

        # Apply any class-level content transformations
        return target.preview_write(content=target_content)
