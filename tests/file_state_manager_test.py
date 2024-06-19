import os
import unittest

from wexample_filestate.file_state_manager import FileStateManager


class TestFileStateManagerTest(unittest.TestCase):

    def setUp(self):
        self.state_manager = FileStateManager(root=os.path.join(os.curdir, 'tests', 'resources'))

    def test_file_permissions(self):
        self.state_manager.configure({
            'files': [
                {
                    'name': 'simple-text.txt',
                    'mode': '0644'
                }
            ]
        })

        self.state_manager.dry_run()

        self.assertTrue(self.state_manager.root.path.is_dir())


if __name__ == '__main__':
    unittest.main()
