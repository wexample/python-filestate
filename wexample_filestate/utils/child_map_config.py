import copy
import os
import re
from pathlib import Path
from typing import List

from wexample_filestate.const.types_state_items import TargetFileOrDirectory
from wexample_filestate.helpers.config_helper import config_has_item_type
from wexample_filestate.item.abstract_file_state_item import AbstractStateItem
from wexample_filestate.utils.child_config import ChildConfig


class ChildMapConfig(ChildConfig):

    def parse_config(
        self,
        target: TargetFileOrDirectory,
    ) -> List[AbstractStateItem]:

        if "name_pattern" in self.config:
            base_path = target.get_resolved()
            children = []

            pattern = re.compile(self.config["name_pattern"])
            for file in os.listdir(base_path):
                if pattern.match(file):
                    path = Path(f"{base_path}{file}")

                    if "type" not in self.config or config_has_item_type(self.config, path):
                        item_config_copy = copy.deepcopy(self.config)
                        item_config_copy["name"] = file

                        children.extend(
                            ChildConfig(config=item_config_copy).parse_config(
                                target=target,
                            )
                        )

            return children

        return super().parse_config(target)
