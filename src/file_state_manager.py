from typing import Optional

import yaml
from pydantic import BaseModel

from src.result.file_state_dry_run_result import FileStateDryRunResult


class FileStateManager(BaseModel):
    root_directory: str
    _config: Optional[dict] = None

    @property
    def config(self) -> Optional[dict]:
        return self._config

    @config.setter
    def config(self, value: dict):
        self._config = value

    def configure(self, config: dict):
        self.config = config

    def configure_from_file(self, file_path: str):
        with open(file_path, 'r') as file:
            self.config = yaml.safe_load(file)

    def dry_run(self):
        # Implement dry run logic here
        # This function should return an object that can be printed to show what changes would be made
        return FileStateDryRunResult(self.config)

    def succeed(self):
        # Implement logic to check if the configuration can be successfully applied
        return True  # Return True if successful, False otherwise

    def apply(self):
        # Implement the logic to apply the configuration here
        pass
