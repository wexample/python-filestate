import os
import unittest
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from wexample_filestate.file_state_manager import FileStateManager


class AbstractStateManagerTest(unittest.TestCase):
    state_manager: "FileStateManager"

    def setUp(self) -> None:
        from wexample_filestate.file_state_manager import FileStateManager

        self.state_manager = FileStateManager.create_from_path(path=os.path.join(os.curdir, 'tests', 'resources'))
