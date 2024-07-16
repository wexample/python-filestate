from __future__ import annotations

import os
from typing import Optional, TYPE_CHECKING, List, Type

from pydantic import BaseModel

from wexample_filestate.const.enums import DiskItemType
from wexample_filestate.const.types import StateItemConfig
from wexample_filestate.item.file_state_item_directory_target import FileStateItemDirectoryTarget
from wexample_filestate.options.class_option import ClassOption

if TYPE_CHECKING:
    from wexample_filestate.item.abstract_file_state_item import AbstractStateItem
    from wexample_filestate.const.types_state_items import TargetFileOrDirectory


class ChildConfig(BaseModel):
    config: Optional[StateItemConfig] = None

    def parse_config(
        self,
        target: TargetFileOrDirectory,
    ) -> List[AbstractStateItem]:
        base_path = target.get_resolved()

        if "type" not in self.config:
            self.config["type"] = DiskItemType.FILE if base_path.is_file() else DiskItemType.DIRECTORY

        if "class" in self.config:
            return [self.config["class"](base_path=base_path, config=self.config, parent=target)]

        from wexample_filestate.item.file_state_item_file_target import FileStateItemFileTarget

        is_file = self.config.get("type") == DiskItemType.FILE or (
            "name" in self.config and isinstance(self.config["name"], str) and os.path.isfile(self.config["name"])
        )

        if is_file:
            state_item = FileStateItemFileTarget(base_path=base_path, config=self.config, parent=target)
        else:
            # Directories and undefined files.
            state_item = FileStateItemDirectoryTarget(base_path=base_path, config=self.config, parent=target)

        return [state_item]
