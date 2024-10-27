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

    def test_configure_name(self):
        self.state_manager.configure({
            "name": "yes"
        })

    def test_configure_unexpected(self):
        from wexample_config.exception.option import InvalidOptionException

        with self.assertRaises(InvalidOptionException):
            self.state_manager.configure({
                "unexpected_option": "yes"
            })
