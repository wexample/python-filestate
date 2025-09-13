from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_config.const.types import DictConfig
from wexample_filestate.testing.test_abstract_operation import TestAbstractOperation

if TYPE_CHECKING:
    from wexample_config.const.types import DictConfig


class TestFileDeleteOperation(TestAbstractOperation):
    def _operation_test_assert_applied(self) -> None:
        from wexample_filestate.const.test import TEST_FILE_NAME_SIMPLE_TEXT

        target = self.state_manager.find_by_name(TEST_FILE_NAME_SIMPLE_TEXT)
        assert target is not None, "Target file not found"
        assert not target.get_path().exists(), "The file should not exist"

    def _operation_test_assert_initial(self) -> None:
        from wexample_filestate.const.test import TEST_FILE_NAME_SIMPLE_TEXT

        target = self.state_manager.find_by_name(TEST_FILE_NAME_SIMPLE_TEXT)
        assert target is not None, "Target file not found"
        assert target.get_path().exists(), "The file should exist"

    def _operation_test_setup_configuration(self) -> DictConfig | None:
        from wexample_filestate.const.test import TEST_FILE_NAME_SIMPLE_TEXT

        return {
            "children": [
                {
                    "name": TEST_FILE_NAME_SIMPLE_TEXT,
                    "should_exist": False,
                }
            ]
        }
