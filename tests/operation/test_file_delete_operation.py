import os
from typing import Optional

from wexample_config.const.types import DictConfig
from wexample_filestate.const.test import TEST_FILE_NAME_SIMPLE_TEXT
from wexample_filestate.test.test_abstract_operation import TestAbstractOperation


class TestFileDeleteOperation(TestAbstractOperation):
    def _operation_test_setup_configuration(self) -> Optional[DictConfig]:
        return {
            'children': [
                {
                    'name': TEST_FILE_NAME_SIMPLE_TEXT,
                    'should_exist': False,
                }
            ]
        }

    def _operation_test_assert_initial(self) -> None:
        assert os.path.exists(self.state_manager.find_by_name(TEST_FILE_NAME_SIMPLE_TEXT).get_resolved())
        "The file should exist"

    def _operation_test_assert_applied(self):
        assert os.path.exists(self.state_manager.find_by_name(TEST_FILE_NAME_SIMPLE_TEXT).get_resolved()) is False
        "The file should not exist"
