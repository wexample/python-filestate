from __future__ import annotations

from typing import List
from pydantic import BaseModel

from wexample_filestate.item.abstract_item_target import AbstractItemTarget
from wexample_filestate.operation.abstract_operation import AbstractOperation

class AbstractResult(BaseModel):
    state_manager: "AbstractItemTarget"
    operations: List[AbstractOperation] = []
    rollback: bool = False

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}>"

    def __str__(self) -> str:
        return f"{self.__repr__}"

    def apply_with_dependencies(
            self,
            operation: "AbstractOperation",
            dry_run: bool = False,
            rollback: bool = False
    ) -> None:
        from wexample_helpers.helpers.cli import cli_make_clickable_path

        # Retrieve dependencies based on rollback mode
        dependencies = operation.dependencies()
        dependencies = reversed(dependencies) if rollback else dependencies

        # Execute the main operation before dependencies if rollback, otherwise after dependencies
        if rollback and operation not in self._executed_operations:
            operation.undo()
            operation.applied = False
            self._executed_operations.append(operation)

        # Apply dependencies in the specified order
        for dependency_class in dependencies:
            dependency = self._find_dependency(dependency_class)
            if dependency is not None and dependency not in self._executed_operations:
                self.apply_with_dependencies(
                    operation=dependency,
                    rollback=rollback
                )

        # Execute the main operation after dependencies if not rollback
        if not rollback and operation not in self._executed_operations:
            self.state_manager.io.title("TASK")
            self._apply_single_operation(operation=operation)

            operation.applied = True
            self._executed_operations.append(operation)

            self.state_manager.io.task(
                message=f"{operation.target.get_item_title()}:\n"
                        f"    → {operation.description()}\n"
                        f"    → {cli_make_clickable_path(operation.target.get_resolved())}\n"
                        f"    ⋮ Before: {operation.describe_before()}\n"
                        f"    ⋮ After: {operation.describe_after()}",
            )

    def apply_operations(self) -> None:
        self._executed_operations = []

        # Define order of operations based on rollback mode
        operations = reversed(self.operations) if self.rollback else self.operations

        # Apply each operation with its dependencies in the correct order
        for operation in operations:
            self.apply_with_dependencies(
                operation=operation,
                dry_run=True,
                rollback=self.rollback)
