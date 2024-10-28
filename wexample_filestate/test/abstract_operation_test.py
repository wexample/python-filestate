from abc import abstractmethod, ABC
from typing import TYPE_CHECKING, Type

from wexample_filestate.test.abstract_state_manager_test import AbstractStateManagerTest

if TYPE_CHECKING:
    from wexample_filestate.operation.abstract_operation import AbstractOperation
    from wexample_filestate.result.file_state_dry_run_result import FileStateDryRunResult


class AbstractOperationTest(AbstractStateManagerTest, ABC):
    @abstractmethod
    def get_operation(self) -> Type["AbstractOperation"]:
        pass

    def test_apply(self) -> None:
        self._operation_test_setup()
        self._operation_test_assert_initial()
        self._operation_test_dry_run()
        self._operation_test_apply()
        self._operation_test_assert_applied()
        self._operation_test_rollback()
        self._operation_test_assert_rollback()

    def _dry_run_and_count_operations(self, operations_count: int) -> "FileStateDryRunResult":
        result = self.state_manager.dry_run()
        result.print()

        assert len(result.operations) == operations_count
        assert len(result.to_prompt_responses()) == operations_count

        return result

    def _operation_get_count(self) -> int:
        return 1

    @abstractmethod
    def _operation_test_setup(self) -> None:
        pass

    def _operation_test_assert_initial(self) -> None:
        self._dry_run_and_count_operations(
            operations_count=self._operation_get_count()
        )

    def _operation_test_dry_run(self) -> None:
        self._dry_run_and_count_operations(
            operations_count=self._operation_get_count()
        )

    def _operation_test_apply(self) -> None:
        self.state_manager.apply()

    @abstractmethod
    def _operation_test_assert_applied(self) -> None:
        pass

    def _operation_test_rollback(self) -> None:
        self.state_manager.rollback().print()

    def _operation_test_assert_rollback(self):
        # Rerun initial checkup
        self._operation_test_assert_initial()
