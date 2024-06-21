import os
import unittest

from wexample_filestate.file_state_manager import FileStateManager
from wexample_filestate.result.file_state_dry_run_result import FileStateDryRunResult


class TestFileStateManagerTest(unittest.TestCase):
    file_name_simple_text = 'simple-text.txt'

    def setUp(self):
        self.state_manager = FileStateManager(root=os.path.join(os.curdir, 'tests', 'resources'))

    def tearDown(self):
        self.state_manager.rollback().print()

    def test_change_mode_operation(self):
        self.state_manager.configure({
            'children': [
                {
                    'name': self.file_name_simple_text,
                    'mode': '644'
                },
            ]
        })

        self.assertTrue(self.state_manager.root.path.is_dir())

        self._dry_run_and_count_operations(operations_count=1)

        target = self.state_manager.target.find_by_name(self.file_name_simple_text)
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

    def _dry_run_and_count_operations(self, operations_count: int) -> FileStateDryRunResult:
        result = self.state_manager.dry_run()
        result.print()

        self.assertEqual(
            len(result.operations),
            operations_count
        )

        self.assertEqual(
            len(result.to_prompt_responses()),
            operations_count
        )

        return result

    def test_file_create_operation(self):
        missing_file_name = 'simple-text-missing.txt'
        missing_dir_name = 'simple-directory-missing'

        self.state_manager.configure({
            'children': [
                {
                    'name': missing_dir_name,
                    'should_exist': True,
                    'type': 'dir'
                },
                {
                    'name': missing_file_name,
                    'should_exist': True,
                    'type': 'file'
                }
            ]
        })

        target_dir = self.state_manager.target.find_by_name(missing_dir_name)
        target_file = self.state_manager.target.find_by_name(missing_file_name)

        self.assertFalse(
            os.path.exists(
                target_dir.path.resolve()
            )
        )

        self.assertFalse(
            os.path.exists(
                target_file.path.resolve()
            )
        )

        self._dry_run_and_count_operations(operations_count=2)

        self.state_manager.apply()

        self.assertTrue(
            os.path.exists(
                target_dir.path.resolve()
            )
        )

        self.assertTrue(
            os.path.exists(
                target_file.path.resolve()
            )
        )

    def test_file_delete_operation(self):
        self.state_manager.configure({
            'children': [
                {
                    'name': self.file_name_simple_text,
                    'should_exist': False,
                }
            ]
        })

        target = self.state_manager.target.find_by_name(self.file_name_simple_text)

        self.assertTrue(
            os.path.exists(
                target.path.resolve()
            )
        )

        self._dry_run_and_count_operations(operations_count=1)

        self.state_manager.apply()

        self.assertFalse(
            os.path.exists(
                target.path.resolve()
            )
        )


if __name__ == '__main__':
    unittest.main()
