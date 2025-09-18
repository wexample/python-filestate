from __future__ import annotations

from typing import Any

from pydantic import ConfigDict

from wexample_config.config_value.config_value import ConfigValue
from wexample_filestate.config_option.text_config_option import TextConfigOption
from wexample_filestate.config_option.sort_lines_config_option import SortLinesConfigOption
from wexample_filestate.config_option.unique_lines_config_option import UniqueLinesConfigOption
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
            TextConfigOption.get_name(): self.text,
            SortLinesConfigOption.get_name(): self.sort_lines,
            UniqueLinesConfigOption.get_name(): self.unique_lines,
        }

    def build_content(self) -> str | None:
        return self.text

    def _create_default_raw(self, raw: Any) -> str:
        return ""
