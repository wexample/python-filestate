from __future__ import annotations

import os
import re
from pathlib import Path
from typing import List, Union, cast, Optional, TYPE_CHECKING

from wexample_filestate.const.enums import DiskItemType
from wexample_filestate.const.types import StateItemConfig
from wexample_filestate.helpers.config_helper import config_has_item_type
from wexample_filestate.item.file_state_item_directory import FileStateItemDirectory
from wexample_filestate.item.mixins.state_item_target_mixin import StateItemTargetMixin
from wexample_filestate.result.abstract_result import AbstractResult

if TYPE_CHECKING:
    from wexample_filestate.item.abstract_file_state_item import AbstractStateItem


class FileStateItemDirectoryTarget(FileStateItemDirectory, StateItemTargetMixin):
    config: Optional[StateItemConfig] = None
    _children: List["AbstractStateItem"]

    def __init__(self, **data):
        super().__init__(**data)
        StateItemTargetMixin.__init__(self, **data)

    @property
    def children(self) -> List["AbstractStateItem"]:
        return self._children

    def configure(self, config: Optional[StateItemConfig] = None) -> None:
        super().configure(config)
        self._children = []

        if not config:
            return

        base_path = self.get_resolved()
        if 'children' in config:
            for item_config in config['children']:
                if "name_pattern" in item_config:
                    pattern = re.compile(item_config['name_pattern'])
                    for file in os.listdir(base_path):
                        if pattern.match(file):
                            path = Path(f"{base_path}{file}")

                            if "type" not in item_config or config_has_item_type(item_config, path):
                                item_config_copy = item_config.copy()
                                item_config_copy["name"] = file

                                if "type" not in item_config_copy:
                                    item_config_copy["type"] = \
                                        DiskItemType.FILE if path.is_file() else DiskItemType.DIRECTORY

                                self.children.append(
                                    self.state_manager.state_item_target_from_base_path(
                                        parent=self,
                                        base_path=base_path,
                                        config=item_config_copy
                                    )
                                )
                else:
                    self.children.append(
                        self.state_manager.state_item_target_from_base_path(
                            parent=self,
                            base_path=base_path,
                            config=item_config)
                    )

    def build_operations(self, result: AbstractResult):
        super().build_operations(result)
        from wexample_filestate.item.file_state_item_file_target import FileStateItemFileTarget

        for item in self.children:
            cast(Union[FileStateItemDirectoryTarget, FileStateItemFileTarget], item).build_operations(result)

    def find_by_name(self, name: str) -> Optional["AbstractStateItem"]:
        for child in self.children:
            if child.name == name:
                return child

        return None
