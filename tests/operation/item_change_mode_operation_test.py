from typing import Type
from wexample_filestate.operation.item_change_mode_operation import ItemChangeModeOperation
from wexample_filestate.test.abstract_operation_test import AbstractOperationTest


class ItemChangeModeOperationTest(AbstractOperationTest):
    def get_operation(self) -> Type[ItemChangeModeOperation]:
        return ItemChangeModeOperation

    def test_apply(self) -> None:
        pass
