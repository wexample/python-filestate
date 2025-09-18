from __future__ import annotations

from typing import Any

from pydantic import ConfigDict

from wexample_config.config_value.config_value import ConfigValue
from wexample_filestate.config_option.case_format_config_option import CaseFormatConfigOption
from wexample_filestate.config_option.regex_config_option import RegexConfigOption
from wexample_filestate.config_option.prefix_config_option import PrefixConfigOption
from wexample_filestate.config_option.suffix_config_option import SuffixConfigOption
from wexample_helpers.classes.field import public_field
from wexample_helpers.decorator.base_class import base_class


@base_class
class NameFormatConfigValue(ConfigValue):
    raw: Any = public_field(
        default=None, description="Disabled raw value for this config."
    )
    case_format: str | None = public_field(
        default=None,
        description="Case format: uppercase, lowercase, camelCase, snake_case, kebab-case",
    )
    regex: str | None = public_field(
        default=None,
        description="Regular expression pattern the name must match",
    )
    prefix: str | None = public_field(
        default=None,
        description="Required prefix for the name",
    )
    suffix: str | None = public_field(
        default=None,
        description="Required suffix for the name",
    )

    def to_option_raw_value(self) -> ConfigDict:
        return {
            CaseFormatConfigOption.get_name(): self.case_format,
            RegexConfigOption.get_name(): self.regex,
            PrefixConfigOption.get_name(): self.prefix,
            SuffixConfigOption.get_name(): self.suffix,
        }
