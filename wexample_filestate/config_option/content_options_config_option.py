from __future__ import annotations

from typing import Any

from wexample_config.config_option.abstract_config_option import AbstractConfigOption
from wexample_config.config_value.config_value import ConfigValue


class ContentOptionsConfigOption(AbstractConfigOption):
    """Holds a list of content-level operations to apply to a file's textual content.

    Example config:
        { "content_options": ["lines_sort"] }
    """

    OPTION_NAME_LINES_SORT: str = "lines_sort"

    @staticmethod
    def get_raw_value_allowed_type() -> Any:
        # Use ConfigValue to leverage list helpers like has_item_in_list
        return ConfigValue
