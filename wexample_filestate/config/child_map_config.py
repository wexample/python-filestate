import copy
import os
import re
from pathlib import Path
from typing import List, TYPE_CHECKING

from wexample_filestate.config.child_config import ChildConfig
from wexample_filestate.helpers.config_helper import config_has_same_type_as_file

if TYPE_CHECKING:
    from wexample_filestate.item.abstract_state_item import AbstractStateItem
    from wexample_filestate.const.types_state_items import TargetFileOrDirectory


class ChildMapConfig(ChildConfig):
    def build_state_items(
        self,
        target: "TargetFileOrDirectory",
    ) -> List["AbstractStateItem"]:
        if self.config.get("name_pattern"):
            base_path = target.get_resolved()
            children = []

            pattern = re.compile(self.config["name_pattern"])
            for file in os.listdir(base_path):
                if pattern.match(file):
                    path = Path(f"{base_path}{file}")

                    if "type" not in self.config or config_has_same_type_as_file(self.config, path):
                        item_config_copy = copy.deepcopy(self.config)
                        item_config_copy["name"] = file

                        children.extend(
                            ChildConfig(config=item_config_copy).build_state_items(
                                target=target,
                            )
                        )

            return children

        return super().build_state_items(target)
