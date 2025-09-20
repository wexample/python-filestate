from __future__ import annotations

from wexample_filestate.option.name_format.abstract_name_format_child_option import AbstractNameFormatChildOption
from wexample_helpers.decorator.base_class import base_class


@base_class
class SuffixOption(AbstractNameFormatChildOption):
    def get_description(self) -> str:
        return "Enforce suffix requirement for file names"

    def validate_name(self, name: str) -> bool:
        """Validate if name ends with the required suffix."""
        if self.get_value().is_none():
            return True
            
        suffix = self.get_value().get_str()
        return name.endswith(suffix)

    def apply_correction(self, name: str) -> str:
        """Apply suffix correction to name."""
        if self.get_value().is_none():
            return name
            
        suffix = self.get_value().get_str()
        if not name.endswith(suffix):
            return name + suffix
        return name
