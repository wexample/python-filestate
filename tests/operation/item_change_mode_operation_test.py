from typing import Type

from wexample_filestate.operation.item_change_mode_operation import ItemChangeModeOperation
from wexample_filestate.test.abstract_operation_test import AbstractOperationTest


class ItemChangeModeOperationTest(AbstractOperationTest):
    def get_operation(self) -> Type[ItemChangeModeOperation]:
        return ItemChangeModeOperation

    def test_apply(self) -> None:
        from wexample_filestate.const.test import TEST_FILE_NAME_SIMPLE_TEXT

        self.state_manager.configure({
            'children': [
                {
                    'name': TEST_FILE_NAME_SIMPLE_TEXT,
                    'mode': '644'
                },
            ]
        })

        self.assertTrue(self.state_manager.path.is_dir())

        self._dry_run_and_count_operations(operations_count=1)

