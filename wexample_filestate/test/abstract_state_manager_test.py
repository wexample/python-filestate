import os
from abc import ABC
from typing import cast

from wexample_filestate.file_state_manager import FileStateManager


class AbstractStateManagerTest(ABC):
    state_manager: "FileStateManager"

    def _get_package_root_path(self) -> str:
        return os.path.join(os.path.realpath(os.path.dirname(__file__)), "..", "..", "")

    def _get_test_state_manager_path(self) -> str:
        return os.path.join(self._get_package_root_path(), "tests", "resources", "")

    def setup_method(self) -> None:
        from wexample_filestate.file_state_manager import FileStateManager

        self.state_manager = cast(
            FileStateManager,
            FileStateManager.create_from_path(
                path=self._get_test_state_manager_path(),
            ),
        )
