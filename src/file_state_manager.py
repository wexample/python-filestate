from pathlib import Path
from typing import Optional

import yaml
from pydantic import BaseModel

from src.const.types import FileStringOrPath
from src.helpers.file_helper import file_resolve_path
from src.result.file_state_dry_run_result import FileStateDryRunResult
from src.result.file_state_result import FileStateResult


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
        path = file_resolve_path(path)
        with open(path, 'r') as f:
            self.config = yaml.safe_load(f)

    def dry_run(self) -> FileStateDryRunResult:
        return FileStateDryRunResult()

    def succeed(self) -> bool:
        # Implement logic to check if the configuration can be successfully applied
        return True  # Return True if successful, False otherwise

    def apply(self) -> FileStateResult:
        return FileStateResult()
