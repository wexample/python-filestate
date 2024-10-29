from __future__ import annotations

from wexample_filestate.result.abstract_result import AbstractResult


class FileStateResult(AbstractResult):
    _executed_operations: list

    def apply_with_dependencies(self, operation):
        # For each dependency class required by the current operation
        for dependency_class in operation.dependencies():
            # Find the first operation instance matching the dependency class
            dependency = next(op for op in self.operations if isinstance(op, dependency_class))
            # If the dependency exists and hasn't been executed yet, apply it recursively
            if dependency is not None and dependency not in self._executed_operations:
                self.apply_with_dependencies(dependency)

        # Execute the operation if it hasn't been executed yet
        if operation not in self._executed_operations:
            if not self.rollback:
                operation.apply()
                operation.applied = True
            else:
                operation.undo()
                operation.applied = False
            self._executed_operations.append(operation)

    def apply_operations(self):
        self._executed_operations = []

        # Reverse operations order in rollback mode
        operations = reversed(self.operations) if self.rollback else self.operations

        for operation in operations:
            self.apply_with_dependencies(operation)
            self._executed_operations.append(operation)
