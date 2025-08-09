from typing import Optional, Any

from wexample_filestate.const.test import TEST_FILE_NAME_SIMPLE_TEXT
from wexample_filestate.testing.test_abstract_operation import TestAbstractOperation


class TestShouldExistOption(TestAbstractOperation):
    def _operation_test_setup_configuration(self) -> Optional[Any]:
        from wexample_filestate.config_option.should_exist_config_option import ShouldExistConfigOption

        return {
            ShouldExistConfigOption
        }

    def _operation_get_count(self) -> int:
        return 0

    def _operation_test_assert_initial(self) -> None:
        self._assert_file_exists(
            file_path=self._get_absolute_path_from_state_manager(
                TEST_FILE_NAME_SIMPLE_TEXT
            )
        )

    def _operation_test_assert_applied(self):
        self._assert_file_exists(
            file_path=self._get_absolute_path_from_state_manager(
                TEST_FILE_NAME_SIMPLE_TEXT
            )
        )
