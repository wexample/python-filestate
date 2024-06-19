from typing import Optional, cast

from pydantic import BaseModel, Field

from helpers.state_item_helper import state_item_from_path
from wexample_filestate.item.abstract_file_state_item import AbstractFileStateItem
from wexample_filestate.result.abstract_result import AbstractResult
from wexample_filestate.result.file_state_dry_run_result import FileStateDryRunResult
from wexample_filestate.result.file_state_result import FileStateResult
from wexample_helpers.const.types import FileStringOrPath
from wexample_helpers_yaml.helpers.yaml_helpers import yaml_load


class FileStateManager(BaseModel):
    root: AbstractFileStateItem = Field(..., description="Actual root item definition")
    _target: AbstractFileStateItem = None

    def __init__(self, root: str, config: Optional[dict] = None):
        super().__init__(root=state_item_from_path(root))

        self._target = AbstractFileStateItem(path=root)

        if config:
            self.configure(config)

    def configure(self, config: dict):
        self._target.configure(config)

    def configure_from_file(self, path: FileStringOrPath):
        self.configure(yaml_load(path))

    def run(self, result: AbstractResult) -> AbstractResult:
        return result

    def dry_run(self) -> FileStateDryRunResult:
        return cast(FileStateDryRunResult, self.run(FileStateDryRunResult()))

    def apply(self) -> FileStateResult:
        return cast(FileStateResult, self.run(FileStateResult()))
