from __future__ import annotations

import os
from typing import Optional, TYPE_CHECKING, List, Type

from pydantic import BaseModel

from wexample_config.const.types import DictConfig
from wexample_filestate.const.disk import DiskItemType
from wexample_filestate.item.file_state_item_directory_target import FileStateItemDirectoryTarget

if TYPE_CHECKING:
    from wexample_filestate.item.abstract_state_item import AbstractStateItem
    from wexample_filestate.const.types_state_items import TargetFileOrDirectory


class ChildConfig(BaseModel):
    config: Optional[DictConfig] = None

    def parse_config(
        self,
        target: TargetFileOrDirectory,
    ) -> List["AbstractStateItem"]:
        base_path = target.get_resolved()

        if "type" not in self.config:
            self.config["type"] = DiskItemType.FILE if target.is_file() else DiskItemType.DIRECTORY

        is_file = self.config.get("type") == DiskItemType.FILE or (
            "name" in self.config and isinstance(self.config["name"], str) and os.path.isfile(self.config["name"])
        )

        if is_file:
            pass
        else:
            # Directories and undefined files.
            state_item = FileStateItemDirectoryTarget(base_path=base_path, config=self.config, parent=target)

        return [state_item]
