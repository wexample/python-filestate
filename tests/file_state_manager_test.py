import os
import unittest

from wexample_filestate.file_state_manager import FileStateManager
from wexample_filestate.result.file_state_dry_run_result import FileStateDryRunResult


class TestFileStateManagerTest(unittest.TestCase):

    def setUp(self):
        self.state_manager = FileStateManager(root=os.path.join(os.curdir, 'tests', 'resources'))

    def tearDown(self):
        self.state_manager.rollback().print()

    def test_change_mode_operation(self):
        self.state_manager.configure({
            'children': [
                {
                    'name': 'simple-text.txt',
                    'mode': '644'
                },
            ]
        })

        self.assertTrue(self.state_manager.root.path.is_dir())

        self._dry_run_and_count_operations(operations_count=1)

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

        self.state_manager.configure({
            'children': [
                {
                    'name': missing_file_name,
                    'mode': '0644',
                    'should_exists': True,
                    'type': 'file'
                }
            ]
        })

        self.assertFalse(
            os.path.exists(
                self.state_manager.target.find_by_name(missing_file_name).path.resolve()
            )
        )

        self._dry_run_and_count_operations(operations_count=1)

        self.state_manager.apply()

        self.assertTrue(
            os.path.exists(
                self.state_manager.target.find_by_name(missing_file_name).path.resolve()
            )
        )


if __name__ == '__main__':
    unittest.main()
