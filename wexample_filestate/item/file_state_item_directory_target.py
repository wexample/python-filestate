from __future__ import annotations

import os

from typing import Optional, List
from wexample_config.const.types import DictConfig
from wexample_filestate.item.abstract_state_item import AbstractStateItem
from wexample_filestate.item.file_state_item_directory import FileStateItemDirectory
from wexample_filestate.item.mixins.state_item_target_mixin import StateItemTargetMixin


class FileStateItemDirectoryTarget(FileStateItemDirectory, StateItemTargetMixin):
    children: List["AbstractStateItem"] = []

    def configure(self, config: Optional[DictConfig]) -> None:
        from wexample_filestate.utils.child_config import ChildConfig
        super().configure(config)

        if "children" in config:
            import copy

            for item_config in config["children"]:
                if isinstance(item_config, ChildConfig):
                    child_config = item_config
                else:
                    child_config = ChildConfig(config=copy.deepcopy(item_config))

                self.children.extend(
                    child_config.parse_config(
                        target=self,
                    )
                )

    @classmethod
    def create_from_path(
        cls,
        path: str,
        config: Optional[DictConfig] = None,
    ) -> FileStateItemDirectoryTarget:
        from wexample_helpers.helpers.directory_helper import directory_get_base_name, directory_get_parent_path

        config = config or {}

        # If path is a file, ignore file name a keep parent directory.
        if os.path.isfile(path):
            path = os.path.dirname(path)

        config["name"] = directory_get_base_name(path)

        return cls(
            config=config,
            base_path=directory_get_parent_path(path),
        )
