from typing import List, Optional

from wexample_config.config_value.config_value import ConfigValue
from wexample_filestate.config_value.filter.abstract_config_value_filter import AbstractConfigValueFilter


class ItemConfigValue(ConfigValue):
    filters: Optional[List[AbstractConfigValueFilter]] = []

    def render(self) -> str:
        return self.get_str()
