import os
import unittest

from wexample_filestate.file_state_manager import FileStateManager
from wexample_helpers.helpers.file_helper import file_mode_octal_to_num


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

        self.assertTrue(self.state_manager.root.path.is_dir())

        result = self.state_manager.dry_run()

        self.assertGreater(
            len(result.operations),
            0
        )

        responses = result.to_prompt_responses()

        self.state_manager.io.print_responses(
            responses
        )

        self.assertGreater(
            len(responses),
            0
        )

        target = self.state_manager.target.find_by_name('simple-text.txt')
        original_mode = target.source.get_octal_mode()

        self.assertNotEqual(
            original_mode,
            target.mode
        )

        self.state_manager.apply()

        self.assertEqual(
            target.get_octal_mode(),
            target.mode
        )

        os.chmod(
            target.path,
            file_mode_octal_to_num(original_mode)
        )


if __name__ == '__main__':
    unittest.main()
