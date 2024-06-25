from __future__ import annotations

from typing import cast, Optional

from pydantic import BaseModel, Field

from wexample_filestate.const.types import StateItemConfig
from wexample_filestate.const.types_state_items import SourceFileOrDirectory, TargetFileOrDirectory
from wexample_filestate.item.abstract_file_state_item import AbstractFileStateItem
from wexample_filestate.result.abstract_result import AbstractResult
from wexample_filestate.result.file_state_dry_run_result import FileStateDryRunResult
from wexample_filestate.result.file_state_result import FileStateResult
from wexample_helpers.const.types import FileStringOrPath
from wexample_helpers.helpers.file_helper import file_resolve_path
from wexample_helpers_yaml.helpers.yaml_helpers import yaml_read
from wexample_prompt.io_manager import IOManager
from wexample_filestate.item.file_state_item_file_target import FileStateItemFileTarget
from wexample_filestate.item.file_state_item_directory_target import FileStateItemDirectoryTarget
from wexample_filestate.item.file_state_item_file_source import FileStateItemFileSource
from wexample_filestate.item.file_state_item_directory_source import FileStateItemDirectorySource


class FileStateManager(BaseModel):
    io: IOManager = Field(
        default_factory=IOManager,
        description="Handles output to print, allow to share it if defined in a parent context")
    root: SourceFileOrDirectory = Field(
        ...,
        description="Current root item definition")
    _target: TargetFileOrDirectory = None
    _last_result: Optional[AbstractResult] = None

    def __init__(self, root: FileStringOrPath, config: Optional[StateItemConfig] = None, io: IOManager = None):
        super().__init__(root=self.state_item_source_from_path(root))

        self.io = io or IOManager()

        self.configure(config)

    @property
    def target(self) -> TargetFileOrDirectory:
        return self._target

    def rollback(self) -> FileStateResult:
        result = FileStateResult(state_manager=self, rollback=True)

        if self._last_result:
            for operation in self._last_result.operations:
                if operation.applied:
                    result.operations.append(operation)

        result.apply_operations()
        self._last_result = result

        return result

    def configure(self, config: Optional[StateItemConfig] = None):
        self._target = cast(
            FileStateItemDirectoryTarget,
            self.state_item_target_from_path(
                path=self.root.path
            )
        )

        self._target.configure(config)

    def configure_from_file(self, path: FileStringOrPath):
        self.configure(yaml_read(path))

    def run(self, result: AbstractResult) -> AbstractResult:
        self._target.build_operations(result)
        self._last_result = result

        return self._last_result

    def dry_run(self) -> FileStateDryRunResult:
        return cast(FileStateDryRunResult, self.run(FileStateDryRunResult(state_manager=self)))

    def apply(self) -> FileStateResult:
        return cast(FileStateResult, self.run(FileStateResult(state_manager=self))).apply_operations()

    def state_item_source_from_path(self, path: FileStringOrPath) -> AbstractFileStateItem:
        from wexample_filestate.item.file_state_item_directory_source import FileStateItemDirectorySource
        from wexample_filestate.item.file_state_item_file_source import FileStateItemFileSource
        resolved_path = file_resolve_path(path)
        if resolved_path.is_file():
            return FileStateItemFileSource(state_manager=self, path=resolved_path)
        elif resolved_path.is_dir():
            return FileStateItemDirectorySource(state_manager=self, path=resolved_path)
        else:
            raise ValueError('Root path should be a valid file or directory')

    def state_item_target_from_path(
        self,
        path: FileStringOrPath,
        config: Optional[StateItemConfig] = None,
        parent: Optional[TargetFileOrDirectory] = None) -> AbstractFileStateItem:
        from wexample_filestate.item.file_state_item_directory_target import FileStateItemDirectoryTarget
        from wexample_filestate.item.file_state_item_file_target import FileStateItemFileTarget
        resolved_path = file_resolve_path(path)

        if resolved_path.is_file() or (config and 'type' in config and config['type'] == 'file'):
            return FileStateItemFileTarget(state_manager=self, path=resolved_path, config=config, parent=parent)
        # Directories and undefined files.
        return FileStateItemDirectoryTarget(state_manager=self, path=resolved_path, config=config, parent=parent)


# Rebuild classes that point back to manager.
FileStateItemFileTarget.model_rebuild()
FileStateItemDirectoryTarget.model_rebuild()
FileStateItemFileSource.model_rebuild()
FileStateItemDirectorySource.model_rebuild()
FileStateDryRunResult.model_rebuild()
FileStateResult.model_rebuild()
