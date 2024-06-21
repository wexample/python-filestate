from __future__ import annotations

from wexample_filestate.result.abstract_result import AbstractResult


class FileStateResult(AbstractResult):
    def apply_operations(self):
        for operation in self.operations:
            if not self.rollback:
                operation.apply()
                operation.applied = True
            else:
                operation.undo()
                operation.applied = False
