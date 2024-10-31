from typing import Type
from wexample_filestate.item.file_state_item_directory_target import FileStateItemDirectoryTarget
from wexample_helpers.test.abstract_test_helpers import AbstractTestHelpers


class TestFileStateManager(AbstractTestHelpers):
    def test_types(self):
        from wexample_filestate.file_state_manager import FileStateManager

        class TestClass(FileStateManager):
            pass

        self._test_type_validate_or_fail(
            success_cases=[
                (TestClass, Type[FileStateItemDirectoryTarget])
            ]
        )
