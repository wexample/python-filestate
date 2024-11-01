from __future__ import annotations

from wexample_filestate.result.abstract_result import AbstractResult


class FileStateResult(AbstractResult):
    _executed_operations: list = []

    def apply_with_dependencies(self, operation, rollback: bool = False):
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
            dependency = next(
                op for op in self.operations if isinstance(op, dependency_class)
            )
            if dependency is not None and dependency not in self._executed_operations:
                self.apply_with_dependencies(dependency, rollback=rollback)

        # Execute the main operation after dependencies if not rollback
        if not rollback and operation not in self._executed_operations:
            operation.apply()
            operation.applied = True
            self._executed_operations.append(operation)

    def apply_operations(self):
        self._executed_operations = []

        # Define order of operations based on rollback mode
        operations = reversed(self.operations) if self.rollback else self.operations

        # Apply each operation with its dependencies in the correct order
        for operation in operations:
            self.apply_with_dependencies(operation, rollback=self.rollback)
