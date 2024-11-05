from typing import Optional

from wexample_config.const.types import DictConfig
from wexample_filestate.const.types_state_items import TargetFileOrDirectoryType
from wexample_filestate.test.test_abstract_operation import TestAbstractOperation
from wexample_filestate.const.test import TEST_FILE_NAME_SIMPLE_TEXT


class TestItemChangeModeOperation(TestAbstractOperation):
    def _get_target(self) -> Optional["TargetFileOrDirectoryType"]:
        return self.state_manager.find_by_name(TEST_FILE_NAME_SIMPLE_TEXT)

    def _get_expected_mode(self) -> str:
        from wexample_filestate.config_option.mode_config_option import ModeConfigOption
        target = self.state_manager.find_by_name(TEST_FILE_NAME_SIMPLE_TEXT)
        return target.get_option_value(ModeConfigOption).get_str()

    def _operation_test_setup_configuration(self) -> Optional[DictConfig]:
        return {
            'children': [
                {
                    'name': TEST_FILE_NAME_SIMPLE_TEXT,
                    'mode': '644'
                },
            ]
        }

    def _operation_test_assert_initial(self) -> None:
        assert self.state_manager.get_path().is_dir() is True
        assert self._get_target().source.get_octal_mode() != self._get_expected_mode()

    def _operation_test_assert_applied(self):
        assert self._get_target().get_octal_mode() == self._get_expected_mode()
