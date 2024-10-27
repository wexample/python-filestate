import os
import unittest

from wexample_filestate.file_state_manager import FileStateManager


class TestFileStateManagerTest(unittest.TestCase):

    def setUp(self):
        self.state_manager = FileStateManager.create_from_path(path=os.path.join(os.curdir, 'tests', 'resources'))

    def test_setup(self):
        self.assertIsNotNone(
            self.state_manager
        )
