from typing import Type

from wexample_config.option.abstract_option import AbstractOption
from wexample_filestate.config_value.item_config_value import ItemConfigValue


class AbstractItemOption(AbstractOption):
    def get_value_class_type(self) -> Type:
        return ItemConfigValue
