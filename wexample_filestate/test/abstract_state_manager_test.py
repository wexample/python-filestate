import os
from abc import ABC
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from wexample_filestate.file_state_manager import FileStateManager


class AbstractStateManagerTest(ABC):
    state_manager: "FileStateManager"

    def get_package_root_path(self) -> str:
        return os.path.realpath(os.path.dirname(__file__) + '/../../') + os.sep

    def get_package_resources_path(self) -> str:
        return os.path.join(
            self.get_package_root_path(), 'tests', 'resources'
        ) + os.sep

    def setup_method(self) -> None:
        from wexample_filestate.file_state_manager import FileStateManager

        self.state_manager = FileStateManager.create_from_path(
            path=self.get_package_resources_path())
