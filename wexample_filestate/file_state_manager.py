from typing import cast, Optional

from pydantic import BaseModel, Field

from wexample_filestate.const.types_state_items import SourceFileOrDirectory, TargetFileOrDirectory
from wexample_filestate.helpers.state_item_helper import state_item_source_from_path
from wexample_filestate.result.abstract_result import AbstractResult
from wexample_filestate.result.file_state_dry_run_result import FileStateDryRunResult


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

    def run(self, result: AbstractResult) -> AbstractResult:
        return result

    def dry_run(self) -> FileStateDryRunResult:
        return cast(FileStateDryRunResult, self.run(FileStateDryRunResult()))
