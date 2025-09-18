from __future__ import annotations

from typing import TYPE_CHECKING

from tests.package.operation.test_item_change_mode_operation import TestItemChangeModeOperation

from wexample_filestate.option.mode_option import ModeOption
from wexample_filestate.option.name_option import NameOption

if TYPE_CHECKING:
    from wexample_config.const.types import DictConfig


class TestItemChangeModeOperationDict(TestItemChangeModeOperation):
    def _operation_test_setup_configuration(self) -> DictConfig | None:
        from wexample_filestate.const.test import TEST_FILE_NAME_SIMPLE_TEXT
        from wexample_filestate.config_option.permissions_config_option import PermissionsConfigOption
        from wexample_filestate.config_option.recursive_config_option import RecursiveConfigOption

        return {
            "children": [
                {
                    NameOption.get_name(): TEST_FILE_NAME_SIMPLE_TEXT,
                    ModeOption.get_name(): {
                        PermissionsConfigOption.get_name(): "755",
                        RecursiveConfigOption.get_name(): True
                    }
                },
            ]
        }
