from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_filestate.testing.abstract_test_operation import AbstractTestOperation

if TYPE_CHECKING:
    from wexample_config.const.types import DictConfig


class TestContentOptionCombined(AbstractTestOperation):
    """Test content + text combination with both sort_lines and unique_lines enabled."""
    test_content: str = "zebra\napple\nbanana\napple\ncherry\nbanana"
    expected_content: str = "apple\nbanana\ncherry\nzebra"


    def _operation_test_assert_applied(self) -> None:
        from wexample_filestate.const.test import TEST_FILE_NAME_SIMPLE_TEXT

        self._assert_file_content_equals(
            file_path=self._get_absolute_path_from_state_manager(
                TEST_FILE_NAME_SIMPLE_TEXT
            ),
            expected_value=self.expected_content,
            positive=True,
        )

    def _operation_test_assert_initial(self) -> None:
        from wexample_filestate.const.test import TEST_FILE_NAME_SIMPLE_TEXT

        self._assert_file_content_equals(
            file_path=self._get_absolute_path_from_state_manager(
                TEST_FILE_NAME_SIMPLE_TEXT
            ),
            expected_value=self.expected_content,
            positive=False,
        )

    def _operation_test_setup_configuration(self) -> DictConfig | None:
        from wexample_filestate.const.disk import DiskItemType
        from wexample_filestate.const.test import TEST_FILE_NAME_SIMPLE_TEXT

        return {
            "children": [
                {
                    "name": TEST_FILE_NAME_SIMPLE_TEXT,
                    "should_exist": True,
                    "type": DiskItemType.FILE,
                    "content": self.test_content,
                    "text": {
                        "sort_lines": True,
                        "unique_lines": True,
                    },
                }
            ]
        }
