from typing import Any, Union, List

from wexample_helpers.const.types import StringKeysDict
from wexample_config.config_option.abstract_config_option import AbstractConfigOption


class YamlFilterConfigOption(AbstractConfigOption):
    @staticmethod
    def get_raw_value_allowed_type() -> Any:
        # Accept both list form ["sort_recursive"] and dict form if extended later
        return Union[List[str], StringKeysDict]
