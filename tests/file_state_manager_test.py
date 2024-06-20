import os
import unittest

from wexample_filestate.file_state_manager import FileStateManager


class TestFileStateManagerTest(unittest.TestCase):

    def setUp(self):
        self.state_manager = FileStateManager(root=os.path.join(os.curdir, 'tests', 'resources'))

    def test_file_permissions(self):
        self.state_manager.configure({
            'children': [
                {
                    'name': 'simple-text.txt',
                    'mode': '644'
                },
                {
                    'name': 'simple-text-missing.txt',
                    'mode': '0644',
                    'should_exists': True,
                    'type': 'file'
                }
            ]
        })


if __name__ == '__main__':
    unittest.main()
