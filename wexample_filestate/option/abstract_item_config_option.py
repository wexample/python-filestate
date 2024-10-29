from typing import Type

from wexample_config.option.abstract_config_option import AbstractConfigOption
from wexample_filestate.config_value.item_config_value import ItemConfigValue


class AbstractItemConfigOption(AbstractConfigOption):
    def get_value_class_type(self) -> Type:
        return ItemConfigValue
