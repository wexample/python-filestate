from __future__ import annotations

from typing import Any, Union

from wexample_config.config_option.abstract_config_option import AbstractConfigOption


class YamlFilterConfigOption(AbstractConfigOption):
    @staticmethod
    def get_raw_value_allowed_type() -> Any:
        from wexample_helpers.const.types import StringKeysDict
        # Accept both list form ["sort_recursive"] and dict form if extended later
        return Union[list[str], StringKeysDict]
