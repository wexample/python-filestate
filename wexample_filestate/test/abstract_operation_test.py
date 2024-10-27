from abc import abstractmethod
from typing import TYPE_CHECKING, Type

from wexample_filestate.test.abstract_state_manager_test import AbstractStateManagerTest

if TYPE_CHECKING:
    from wexample_filestate.operation.abstract_operation import AbstractOperation
    from wexample_filestate.result.file_state_dry_run_result import FileStateDryRunResult


class AbstractOperationTest(AbstractStateManagerTest):
    @abstractmethod
    def get_operation(self) -> Type["AbstractOperation"]:
        pass

    @abstractmethod
    def test_apply(self) -> None:
        pass

    def _dry_run_and_count_operations(self, operations_count: int) -> "FileStateDryRunResult":
        result = self.state_manager.dry_run()
        result.print()

        self.assertEqual(
            len(result.operations),
            operations_count
        )

        self.assertEqual(
            len(result.to_prompt_responses()),
            operations_count
        )

        return result
