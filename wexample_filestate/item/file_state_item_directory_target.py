from __future__ import annotations

import os
import re
from typing import List, Union, cast, Optional

from wexample_filestate.const.types import StateItemConfig
from wexample_filestate.helpers.config_helper import config_has_item_type
from wexample_filestate.item.abstract_file_state_item import AbstractFileStateItem
from wexample_filestate.item.file_state_item_directory import FileStateItemDirectory
from wexample_filestate.item.mixins.state_item_target_mixin import StateItemTargetMixin
from wexample_filestate.result.abstract_result import AbstractResult


class FileStateItemDirectoryTarget(FileStateItemDirectory, StateItemTargetMixin):
    config: Optional[StateItemConfig] = None
    children: List[AbstractFileStateItem] = []

    def __init__(self, **data):
        super().__init__(**data)
        StateItemTargetMixin.__init__(self, **data)

    def configure(self, config: Optional[StateItemConfig] = None) -> None:
        super().configure(config)
        self.children = []

        if not config:
            return

        base_path = self.get_resolved()
        if 'children' in config:
            for item_config in config['children']:
                paths = []

                if "name" in item_config:
                    paths.append(f'{base_path}{item_config["name"]}')

                elif "name_pattern" in item_config:
                    pattern = re.compile(item_config['name_pattern'])
                    for file in os.listdir(base_path):
                        if pattern.match(file):
                            path = f'{base_path}{file}'
                            if ("type" not in item_config) or config_has_item_type(item_config, path):
                                paths.append(path)

                for path in paths:
                    self.children.append(
                        self.state_manager.state_item_target_from_path(
                            parent=self,
                            path=path,
                            config=item_config)
                    )

    def build_operations(self, result: AbstractResult):
        super().build_operations(result)
        from wexample_filestate.item.file_state_item_file_target import FileStateItemFileTarget

        for item in self.children:
            cast(Union[FileStateItemDirectoryTarget, FileStateItemFileTarget], item).build_operations(result)

    def find_by_name(self, name: str) -> Optional[AbstractFileStateItem]:
        for child in self.children:
            if child.name == name:
                return child

        return None
