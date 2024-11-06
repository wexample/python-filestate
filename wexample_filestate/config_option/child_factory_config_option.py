import copy
import os
import re
from pathlib import Path
from typing import Any, TYPE_CHECKING, cast, List

from wexample_config.config_option.abstract_nested_config_option import AbstractNestedConfigOption
from wexample_config.const.types import DictConfig
from wexample_filestate.config_option.mixin.item_config_option_mixin import ItemTreeConfigOptionMixin
from wexample_filestate.config_option.name_pattern_config_option import NamePatternConfigOption

if TYPE_CHECKING:
    from wexample_config.options_provider.abstract_options_provider import AbstractOptionsProvider
    from wexample_filestate.const.types_state_items import TargetFileOrDirectoryType


class ChildFactoryConfigOption(ItemTreeConfigOptionMixin, AbstractNestedConfigOption):
    pattern: DictConfig

    def get_options_providers(self) -> list[type["AbstractOptionsProvider"]]:
        from wexample_filestate.options_provider.default_options_provider import DefaultOptionsProvider

        return [
            DefaultOptionsProvider,
        ]

    @staticmethod
    def get_raw_value_allowed_type() -> Any:
        return DictConfig

    def generate_children(self) -> List["TargetFileOrDirectoryType"]:
        from wexample_filestate.config_option.children_config_option import ChildrenConfigOption

        from wexample_filestate.helpers.config_helper import config_has_same_type_as_file
        parent_children_config = cast(ChildrenConfigOption, self.get_parent())

        config = self.pattern

        children = []
        name_pattern_option_name = NamePatternConfigOption.get_name()
        parent_item = self.get_parent_item()
        if config.get(name_pattern_option_name):
            path = parent_item.get_path()
            if path.exists():
                base_path = parent_item.get_resolved()

                patterns = config[name_pattern_option_name]
                if isinstance(patterns, str):
                    patterns = [patterns]
                for file in os.listdir(base_path):
                    all_match = True
                    for pattern_str in patterns:
                        pattern = re.compile(pattern_str)
                        if not pattern.match(file):
                            all_match = False
                            break

                    if all_match:
                        path = Path(f"{base_path}{file}")

                        if "type" not in config or config_has_same_type_as_file(config, path):
                            item_config_copy = copy.deepcopy(config)

                            if item_config_copy.get("name", None) is None:
                                item_config_copy["name"] = path.name

                            children.append(parent_children_config.create_child_item(
                                child_config=item_config_copy,
                            ))

        return children
