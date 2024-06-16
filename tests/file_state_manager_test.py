import unittest

from src.file_state_manager import FileStateManager


class TestFileStateManagerTest(unittest.TestCase):

    def setUp(self):
        self.state_manager = FileStateManager(root_directory='root/directory/')

    def test_configure(self):
        config = {'files': [{'path': '/path/to/file', 'owner': 'user', 'group': 'group', 'mode': '0644'}]}
        self.state_manager.configure(config)
        self.assertEqual(self.state_manager.config, config)


if __name__ == '__main__':
    unittest.main()
