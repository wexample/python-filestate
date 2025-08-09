from typing import Optional, Any

from wexample_config.const.types import DictConfig
from wexample_filestate.testing.test_abstract_operation import TestAbstractOperation


class TestShouldExistOption(TestAbstractOperation):
    missing_file_name: str = 'simple-text-missing.txt'
    missing_dir_name: str = 'simple-directory-missing'
    existing_file_name: str = 'simple-text.txt'
    existing_dir_name: str = 'collection'

    def _operation_test_setup_configuration(self) -> Optional[Any]:
        return {
            TestShouldExistOption
        }

    def _operation_get_count(self) -> int:
        return 0

    def _operation_test_assert_initial(self) -> None:
        self._assert_file_exists(
            file_path=self._get_absolute_path_from_state_manager(self.existing_file_name)
        )

    def _operation_test_assert_applied(self):
        self._assert_file_exists(
            file_path=self._get_absolute_path_from_state_manager(self.existing_file_name)
        )
