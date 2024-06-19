from pathlib import Path
from typing import Optional
from pydantic import BaseModel
from wexample_filestate.src.result.file_state_dry_run_result import FileStateDryRunResult
from wexample_filestate.src.result.file_state_result import FileStateResult
from wexample_helpers.const.types import FileStringOrPath
from wexample_helpers.helpers.file_helper import file_resolve_path
from wexample_helpers_yaml.helpers.yaml_helpers import yaml_load


class FileStateManager(BaseModel):
    root_directory: Path
    config: dict = {}

    def __init__(self, root_directory: FileStringOrPath, config: Optional[dict] = None):
        super().__init__(
            root_directory=file_resolve_path(root_directory)
        )

        if config:
            self.configure(config)

    def configure(self, config: dict):
        self.config = config

    def configure_from_file(self, path: FileStringOrPath):
        self.config = yaml_load(path)

    def dry_run(self) -> FileStateDryRunResult:
        return FileStateDryRunResult()

    def succeed(self) -> bool:
        # Implement logic to check if the configuration can be successfully applied
        return True  # Return True if successful, False otherwise

    def apply(self) -> FileStateResult:
        return FileStateResult()
