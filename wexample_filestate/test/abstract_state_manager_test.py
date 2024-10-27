import os
import unittest
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from wexample_filestate.file_state_manager import FileStateManager


class AbstractStateManagerTest(unittest.TestCase):
    state_manager: "FileStateManager"

    def setUp(self) -> None:
        from wexample_filestate.file_state_manager import FileStateManager

        current_package_path = os.path.realpath(os.path.dirname(__file__) + '/../../')
        self.state_manager = FileStateManager.create_from_path(
            path=os.path.join(
                current_package_path, 'tests', 'resources'))
