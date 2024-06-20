from __future__ import annotations

from typing import cast, Optional

from pydantic import BaseModel, Field

from wexample_filestate.const.types_state_items import SourceFileOrDirectory, TargetFileOrDirectory
from wexample_filestate.helpers.state_item_helper import state_item_source_from_path
from wexample_filestate.result.abstract_result import AbstractResult
from wexample_filestate.result.file_state_dry_run_result import FileStateDryRunResult
from wexample_filestate.result.file_state_result import FileStateResult
from wexample_helpers.const.types import FileStringOrPath
from wexample_helpers_yaml.helpers.yaml_helpers import yaml_load
# Expected imports for pydantic initialization
from wexample_filestate.item.file_state_item_file_target import FileStateItemFileTarget
from wexample_filestate.item.file_state_item_directory_target import FileStateItemDirectoryTarget
from wexample_filestate.item.file_state_item_file_source import FileStateItemFileSource
from wexample_filestate.item.file_state_item_directory_source import FileStateItemDirectorySource


class FileStateManager(BaseModel):
    root: SourceFileOrDirectory = Field(..., description="Current root item definition")
    _target: TargetFileOrDirectory = None

    def __init__(self, root: str, config: Optional[dict] = None):
        super().__init__(root=state_item_source_from_path(root))

        self._target = self.root.create_target()

        if config:
            self.configure(config)

    def configure(self, config: dict):
        self._target.configure(config)

    def configure_from_file(self, path: FileStringOrPath):
        self.configure(yaml_load(path))

    def run(self, result: AbstractResult) -> AbstractResult:
        self._target.build_operations(result)

        return result

    def dry_run(self) -> FileStateDryRunResult:
        return cast(FileStateDryRunResult, self.run(FileStateDryRunResult()))

    def apply(self) -> FileStateResult:
        return cast(FileStateResult, self.run(FileStateResult()))
