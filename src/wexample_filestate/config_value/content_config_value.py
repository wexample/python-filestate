from __future__ import annotations

from typing import Any

from pydantic import ConfigDict

from wexample_config.config_value.config_value import ConfigValue
from wexample_filestate.option.content.sort_lines_option import SortLinesOption
from wexample_filestate.option.content.unique_lines_option import UniqueLinesOption
from wexample_filestate.option.content.value_option import ValueOption
from wexample_helpers.classes.field import public_field
from wexample_helpers.decorator.base_class import base_class


@base_class
class ContentConfigValue(ConfigValue):
    raw: Any = public_field(
        default=None, description="Disabled raw value for this config."
    )
    text: str | None = public_field(
        default=None,
        description="The text content to write to the file",
    )
    sort_lines: bool | None = public_field(
        default=None,
        description="Sort file lines alphabetically",
    )
    unique_lines: bool | None = public_field(
        default=None,
        description="Remove duplicate lines while preserving order",
    )

    def to_option_raw_value(self) -> ConfigDict:
        return {
            ValueOption.get_name(): self.text,
            SortLinesOption.get_name(): self.sort_lines,
            UniqueLinesOption.get_name(): self.unique_lines,
        }

    def build_content(self) -> str | None:
        return self.text

    def _create_default_raw(self, raw: Any) -> str:
        return ""
