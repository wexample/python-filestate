from __future__ import annotations

from typing import List, Union, cast

from wexample_filestate.const.types import StateItemConfig
from wexample_filestate.item.abstract_file_state_item import AbstractFileStateItem
from wexample_filestate.item.file_state_item_directory import FileStateItemDirectory
from wexample_filestate.item.mixins.state_item_target_mixin import StateItemTargetMixin
from wexample_filestate.result.abstract_result import AbstractResult


class FileStateItemDirectoryTarget(FileStateItemDirectory, StateItemTargetMixin):
    config: StateItemConfig = None
    children: List[AbstractFileStateItem] = []

    def __init__(self, **data):
        super().__init__(**data)
        StateItemTargetMixin.__init__(self, **data)

    def configure(self, config: dict):
        super().configure(config)

        base_path = self.get_resolved()

        if 'children' in config:
            for item_config in config['children']:
                self.children.append(
                    self.state_manager.state_item_target_from_path(
                        path=f'{base_path}{item_config["name"]}',
                        config=item_config)
                )

    def build_operations(self, result: AbstractResult):
        super().build_operations(result)
        from wexample_filestate.item.file_state_item_file_target import FileStateItemFileTarget

        for item in self.children:
            cast(Union[FileStateItemDirectoryTarget, FileStateItemFileTarget], item).build_operations(result)