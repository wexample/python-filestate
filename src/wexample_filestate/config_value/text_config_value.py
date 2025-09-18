from __future__ import annotations

from typing import Any

from pydantic import ConfigDict

from wexample_config.config_value.config_value import ConfigValue
from wexample_filestate.config_option.trim_config_option import TrimConfigOption
from wexample_filestate.config_option.end_new_line_config_option import EndNewLineConfigOption
from wexample_helpers.classes.field import public_field
from wexample_helpers.decorator.base_class import base_class


@base_class
class TextConfigValue(ConfigValue):
    raw: Any = public_field(
        default=None, description="Disabled raw value for this config."
    )
    trim: bool | None = public_field(
        default=None,
        description="Ask to trim leading and trailing whitespace from file content",
    )
    end_new_line: bool | None = public_field(
        default=None,
        description="Ensure file content ends with a newline character",
    )

    def to_option_raw_value(self) -> ConfigDict:
        return {
            TrimConfigOption.get_name(): self.trim,
            EndNewLineConfigOption.get_name(): self.end_new_line,
        }
