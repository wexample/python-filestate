from __future__ import annotations

from wexample_filestate.result.abstract_result import AbstractResult


class FileStateResult(AbstractResult):
    _executed_operations: list

    def apply_with_dependencies(self, operation):
        for dependency_class in operation.dependencies():
            dependency = next(op for op in self.operations if isinstance(op, dependency_class))
            if dependency is not None and dependency not in self._executed_operations:
                self.apply_with_dependencies(dependency)

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

        for operation in self.operations:
            self.apply_with_dependencies(operation)
