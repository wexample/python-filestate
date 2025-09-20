from __future__ import annotations

import re

from wexample_filestate.option.name_format.abstract_name_format_child_option import AbstractNameFormatChildOption
from wexample_helpers.decorator.base_class import base_class


@base_class
class RegexOption(AbstractNameFormatChildOption):
    def get_description(self) -> str:
        return "Enforce regex pattern matching for file names"

    def validate_name(self, name: str) -> bool:
        """Validate if name matches the regex pattern."""
        if self.get_value().is_none():
            return True
            
        regex_pattern = self.get_value().get_str()
        return re.match(regex_pattern, name) is not None

    def apply_correction(self, name: str) -> str:
        """Apply regex correction to name (no automatic correction possible)."""
        # Regex patterns can't be automatically corrected, return name as-is
        # This would require domain-specific logic or user intervention
        return name
