from result.file_state_dry_run_result import FileStateDryRunResult
import yaml
from pydantic import BaseModel


class FileStateManager(BaseModel):
    root_directory: str
    config: dict = {}

    class Config:
        arbitrary_types_allowed = True

    def configure_from_file(self, file_path: str):
        with open(file_path, 'r') as file:
            self.config = yaml.safe_load(file)

    def configure(self, config_dict: dict):
        self.config = config_dict

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
