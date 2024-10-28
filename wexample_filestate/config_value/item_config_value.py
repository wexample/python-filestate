from typing import List, Optional

from typing_extensions import TYPE_CHECKING

from wexample_config.config_value.config_value import ConfigValue
from wexample_filestate.config_value.filter.abstract_config_value_filter import AbstractConfigValueFilter

if TYPE_CHECKING:
    from wexample_filestate.operation.abstract_operation import AbstractOperation


class ItemConfigValue(ConfigValue):
    filters: Optional[List[AbstractConfigValueFilter]] = []

    def render(self, operation: "AbstractOperation") -> str:
        return self.get_str()
