from __future__ import annotations

import copy
import os
from typing import List, Union, cast, Optional, TYPE_CHECKING
from pydantic import Field

from wexample_filestate.const.types import StateItemConfig
from wexample_filestate.item.file_state_item_directory import FileStateItemDirectory
from wexample_filestate.item.mixins.state_item_target_mixin import StateItemTargetMixin
from wexample_filestate.result.abstract_result import AbstractResult
from wexample_helpers.helpers.directory_helper import directory_get_base_name, directory_get_parent_path
from wexample_prompt.io_manager import IOManager
from wexample_helpers.const.types import FileStringOrPath

if TYPE_CHECKING:
    from wexample_filestate.item.abstract_file_state_item import AbstractStateItem
    from wexample_filestate.result.file_state_result import FileStateResult
    from wexample_filestate.result.file_state_dry_run_result import FileStateDryRunResult

class FileStateItemDirectoryTarget(FileStateItemDirectory, StateItemTargetMixin):
    io: IOManager = Field(
        default_factory=IOManager,
        description="Handles output to print, allow to share it if defined in a parent context")
    _children: List["AbstractStateItem"]
    _last_result: Optional[AbstractResult] = None

    def __init__(self, config: Optional[StateItemConfig] = None, **data):
        FileStateItemDirectory.__init__(self, config=config, **data)
        StateItemTargetMixin.__init__(self, config=config, **data)

    @property
    def children(self) -> List["AbstractStateItem"]:
        return self._children

    def configure_from_file(self, path: FileStringOrPath):
        from wexample_helpers_yaml.helpers.yaml_helpers import yaml_read
        self.configure(yaml_read(path))

    def configure(self, config: Optional[StateItemConfig] = None) -> None:
        from wexample_filestate.utils.child_config import ChildConfig

        super().configure(config)
        self._children = []

        if not config:
            return

        if "children" in config:
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
    def create_from_path(
        cls,
        path: str,
        config: Optional[StateItemConfig] = None,
        io: Optional[IOManager] = None
    ) -> FileStateItemDirectoryTarget:
        config = config or {}

        # If path is a file, ignore file name a keep parent directory.
        if os.path.isfile(path):
            path = os.path.dirname(path)

        config["name"] = directory_get_base_name(path)

        return cls(
            config=config,
            base_path=directory_get_parent_path(path),
            io=io or IOManager(),
        )
