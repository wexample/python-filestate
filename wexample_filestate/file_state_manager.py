from typing import cast

from pydantic import BaseModel

from wexample_filestate.result.abstract_result import AbstractResult
from wexample_filestate.result.file_state_dry_run_result import FileStateDryRunResult


class FileStateManager(BaseModel):
    def configure(self, config: dict):
        pass

    def run(self, result: AbstractResult) -> AbstractResult:

        return result

    def dry_run(self) -> FileStateDryRunResult:
        return cast(FileStateDryRunResult, self.run(FileStateDryRunResult()))
