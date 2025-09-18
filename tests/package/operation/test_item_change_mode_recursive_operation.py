from __future__ import annotations

from typing import TYPE_CHECKING

from tests.package.operation.test_item_change_mode_operation import TestItemChangeModeOperation

from wexample_filestate.config_option.recursive_config_option import RecursiveConfigOption
from wexample_filestate.option.mode_option import ModeOption
from wexample_filestate.option.name_option import NameOption

if TYPE_CHECKING:
    from wexample_config.const.types import DictConfig


class TestItemChangeModeRecursiveOperation(TestItemChangeModeOperation):
    def _get_expected_mode(self) -> str:
        from wexample_filestate.option.mode_option import ModeOption
        return self._get_target().get_option_value(ModeOption).get_dict().get('permissions')

    def _operation_test_setup_configuration(self) -> DictConfig | None:
        from wexample_filestate.const.test import TEST_FILE_NAME_SIMPLE_TEXT

        return {
            "children": [
                {
                    NameOption.get_name(): TEST_FILE_NAME_SIMPLE_TEXT,
                    ModeOption.get_name(): {
                        "permissions": "644",
                        RecursiveConfigOption.get_name(): True
                    }
                },
            ]
        }
