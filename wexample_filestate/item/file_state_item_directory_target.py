from __future__ import annotations

import copy
import os
import re
from pathlib import Path
from typing import List, Union, cast, Optional, TYPE_CHECKING
from pydantic import Field

from wexample_filestate.const.enums import DiskItemType
from wexample_filestate.const.types import StateItemConfig
from wexample_filestate.helpers.config_helper import config_has_item_type
from wexample_filestate.item.file_state_item_directory import FileStateItemDirectory
from wexample_filestate.item.mixins.state_item_target_mixin import StateItemTargetMixin
from wexample_filestate.options.children_class_option import ChildrenClassOption
from wexample_filestate.result.abstract_result import AbstractResult
from wexample_helpers.helpers.directory_helper import directory_get_base_name, directory_get_parent_path
from wexample_prompt.io_manager import IOManager
from wexample_helpers.const.types import FileStringOrPath

if TYPE_CHECKING:
    from wexample_filestate.item.abstract_file_state_item import AbstractStateItem
    from wexample_filestate.result.file_state_result import FileStateResult
    from wexample_filestate.result.file_state_dry_run_result import FileStateDryRunResult
    from wexample_filestate.const.types_state_items import TargetFileOrDirectory


class FileStateItemDirectoryTarget(FileStateItemDirectory, StateItemTargetMixin):
    io: IOManager = Field(
        default_factory=IOManager,
        description="Handles output to print, allow to share it if defined in a parent context")
    _children: List["AbstractStateItem"]
    _last_result: Optional[AbstractResult] = None

    def __init__(self, config, **data):
        FileStateItemDirectory.__init__(self, config=config, **data)
        StateItemTargetMixin.__init__(self, config=config, **data)

    @property
    def children(self) -> List["AbstractStateItem"]:
        return self._children

    def configure_from_file(self, path: FileStringOrPath):
        from wexample_helpers_yaml.helpers.yaml_helpers import yaml_read
        self.configure(yaml_read(path))

    def configure(self, config: Optional[StateItemConfig] = None) -> None:
        super().configure(config)
        self._children = []

        if not config:
            return

        children_class_definition = self.get_option_value(ChildrenClassOption)
        base_path = self.get_resolved()
        if "children" in config:
            for item_config in config["children"]:
                if "name_pattern" in item_config:
                    pattern = re.compile(item_config["name_pattern"])
                    for file in os.listdir(base_path):
                        if pattern.match(file):
                            path = Path(f"{base_path}{file}")

                            if "type" not in item_config or config_has_item_type(item_config, path):
                                item_config_copy = copy.deepcopy(item_config)
                                item_config_copy["name"] = file

                                if "type" not in item_config_copy:
                                    item_config_copy["type"] = \
                                        DiskItemType.FILE if path.is_file() else DiskItemType.DIRECTORY

                                self.children.append(
                                    self.state_item_target_from_base_path(
                                        base_path=base_path,
                                        config=item_config_copy,
                                        class_definition=children_class_definition
                                    )
                                )
                else:
                    self.children.append(
                        self.state_item_target_from_base_path(
                            base_path=base_path,
                            config=copy.deepcopy(item_config),
                            class_definition=children_class_definition)
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

    def state_item_target_from_base_path(
        self,
        base_path: FileStringOrPath,
        config: StateItemConfig,
        class_definition: Optional[TargetFileOrDirectory] = None
    ) -> AbstractStateItem:
        if class_definition:
            return class_definition(base_path=base_path, config=config, parent=self)

        from wexample_filestate.item.file_state_item_file_target import FileStateItemFileTarget

        is_file = False
        if 'type' in config:
            is_file = config['type'] == DiskItemType.FILE
        elif 'name' in config and isinstance(config['name'], str):
            is_file = os.path.isfile(config['name'])

        if is_file:
            return FileStateItemFileTarget(base_path=base_path, config=config, parent=self)
        # Directories and undefined files.
        return FileStateItemDirectoryTarget(base_path=base_path, config=config, parent=self)

    def rollback(self) -> FileStateResult:
        result = FileStateResult(state_manager=self, rollback=True)

        if self._last_result:
            for operation in self._last_result.operations:
                if operation.applied:
                    result.operations.append(operation)

        result.apply_operations()
        self._last_result = result

        return result

    def run(self, result: AbstractResult) -> AbstractResult:
        self.build_operations(result)
        self._last_result = result

        return self._last_result

    def dry_run(self) -> "FileStateDryRunResult":
        from wexample_filestate.result.file_state_dry_run_result import FileStateDryRunResult

        return cast(FileStateDryRunResult, self.run(FileStateDryRunResult(state_manager=self)))

    def apply(self) -> "FileStateResult":
        from wexample_filestate.result.file_state_result import FileStateResult
        result = cast(FileStateResult, self.run(FileStateResult(state_manager=self)))
        result.apply_operations()

        return result

    @classmethod
    def create_from_path(cls, path: str, config: Optional[StateItemConfig],
                         io: Optional[IOManager] = None) -> FileStateItemDirectoryTarget:
        config = config or {}
        config["name"] = directory_get_base_name(path)

        return cls(
            config=config,
            base_path=directory_get_parent_path(path),
            io=io or IOManager(),
        )
